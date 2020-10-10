---
layout: post
title: Breaking out of your container
author: Tejas Sanap
---

Making applications for SAP, has always been rooted in **proprietary tools and frameworks**. However, with the onset of the "cloud" movement, SAP is providing its customers and developers, a completely **new services-oriented application model**, that leverages containers and the latest open source standards, for cloud-based applications.

Developers have been able to provide web-based SAP applications, through the use of WebDynpro for a long time. However, that came with its own set of drawbacks. Newer alternatives now use *Fiori-based UI*, with an *OData service*, that transports data back and forth. This approach provides us ample amount of flexibility on the UI side, but for the backend, we are still dependent on *ABAP and the NetWeaver application server*, to execute the business and processing logic for us and the *database server to perform queries* and send data to the Netweaver AS. We also know this as the SAP R3 architecture, where we divide things into the presentation layer, application layer and the database layer.

All of this was fine, until the appearance of HANA database, which provided us with a performance that was an order of magnitude better than its competitors. All of a sudden, the **bottleneck** moved from the database-side to the **application-side**.

With all the speed and power of HANA, it makes much more sense to **do as much processing as possible in the HANA database itself**, at the lowest level; before passing data to the application-side processing logic. *CDS views*, *AMDP* and *stored procedures*, allow us to move much of the processing logic from ABAP or the application-side to the HANA database.

But, wouldn't it be even better, if we could build an application that was completely native to HANA, with no Netweaver AS? This is the exact idea behind the **SAP HANA XS application programming model, where a lightweight javascript runtime is embedded directly into the HANA database**.

This provides us with the ability to **write our database and business logic on the HANA database**, itself. Not only does this provide us with a significant performance boost, but it also comes along with numerous other improvements, on the front of security and operations sides. The SAP HANA XSA application, is also called a MTA application.

This newer model of making applications, is based on an open-source project called **Cloud Foundry**. Cloud Foundry sets an open standard for how applications aimed for cloud-platforms, should be developed and deployed.

This is a huge benefit, as this makes porting applications between SAP cloud and other cloud providers, easy and convienient. SAP HANA XSA is a modded version of vanilla-Cloud Foundry, which comes with a lot of additions that tune it for HANA.

The SAP HANA XSA model provides the following benefits:
1. This application model, takes full advantage of cloud technologies like **microservices and containers**. This adds a new layer of of control, security and ease of operations for the applications we develop. All applications in SAP HANA XSA are deployed as containers, that are built from scratch, each time. These containers are called HDI containers, which stands for, HANA Deployment Infrastructure.
2. With SAP HANA XSA, we see the **BYOL (bring your own language) model** coming to SAP applications. Developers can finally use any language they wish to develop applications and leave ABAP behind. SAP by default, provides support for Java, Node.js and Python runtimes. We can even use R to write SQLScripts.
3. Security and access, take on a much more integrated approach in SAP HANA XSA, where **security objects like roles and priveleges become part of the database itself as HANA artifacts**.

## How does a HDI container interact?

<img src="/assets/images/sap-hana-xsa-synonyms/02-cross-container-scenario.png" width="15%">
<div class="image-caption">
<b>Fig 1.</b> Process.
</div>

Our application may interact with a remote schema on an external database or another external HDI container. To do this, it will need the following:
1. A mechanism that grants users access to database objects based on their roles. These database objects maybe within the application's own schema or they maybe stored in some external source.
2. If the database objects are stored in a remote schema or an external HDI container, we need aliases pointing towards the appropriate database objects.
3. Services that facilitate sending information back and forth, between our application and the remote schema or HDI container

In this transaction, our application which itself is also an HDI container, plays the part of the target system. The remote schema or external HDI container, where the data we want to bring over is stored, plays the part of the source system. We can also call our application HDI container the ego container.

To get a better understanding of how provisioning happens for users based on their roles to schemas, you can refer to [this](https://help.sap.com/viewer/4505d0bdaf4948449b7f7379d24d0f0d/2.0.05/en-US/a260b05631a24a759bba932aa6d81b64.html) document[<sup>1</sup>](#references).

Within any container, there are two kind of technical users:
1. **Object owner**: This user owns all the database objects within the various schemas of the container.
2. **Application user**: This is the end user, who will query for different databse objects, through our application.

Roles and privileges allow us to have a fine control over which users have access to which objects and what actions they can perfrom over those objects. Since, we cannot know before-hand which users might use our applications, these roles and priveleges can be granted to users dynamically during runtime, based on their metadata or credentials.

To access external databse objects we need to link the remote schema or external container, to our application. However, just this is not sufficient, as we still need to know exactly which database artifact, we are looking for in the source system. To link our application to a remote schema or an external container, we use services. Services can be of two types, an existing service provided by the system, or an user-provided one. To point towards a specific database object, we use synonyms, which act as aliases.

In this blog post, we will cover how to read data from another HDI container.

## Basic Premise of our Demo

<img src="/assets/images/sap-hana-xsa-synonyms/01-project-view1.png">
<div class="image-caption">
<b>Fig 2.</b> Source and target applications.
</div>

For example, we will consider a retail chain company. They sell different products in their supermarkets. Each product category becomes a business vertical (or, a department as I call them in this blogpost). Each department has their own application to track and analyse their sales and product variety/inventory. 

While, one department cannot see the sales and product offerings of another department, the higher management that drives the company's operations and growth, needs to be able to see everything from every department. 

For the purposes of our demo, we will take a "Fresh Produce" department application, that contains data about the various fruits they have and the various items they have sold. We will have a "management" application, where the data from the "Fresh Produce" application, needs to be displayed.

Thus, the department application is our source system and the management application is our target system.

## Talking to another HDI container.


To enable cross container access we need to create **roles** that give us access to the data we need. This is done using a HANA database artifact of `.hdbrole` type.

I have created a new HANA database module in our source system with the following folder structure. There is no hard and fast requirement over the folder structure, but being organised always pays off.

<img src="/assets/images/sap-hana-xsa-synonyms/03-source-project-structure.png">
<div class="image-caption">
<b>Fig 3.</b> Source application/Department application structure and data model.
</div>

We will be creating two `.hdbrole` artifacts<sup>[3](https://help.sap.com/viewer/3823b0f33420468ba5f1cf7f59bd6bd9/2.0.04/en-US/625d7733c30b4666b4a522d7fa68a550.html)</sup>. One for the schema owner and another for the application user:
1. freshprod_sales_appuser.hdbrole <br>
```json
{
	"role": {
		"name": "freshprod_sales",
		"object_privileges": [{
			"name": "FRESHPRODUCE_SALES_FRUIT_DETAILS",
			"type": "TABLE",
			"privileges": ["SELECT"]
		}, {
			"name": "FRESHPRODUCE_SALES_FRUIT_SALES",
			"type": "TABLE",
			"privileges": ["SELECT"]
		}]
	}
}
```
2. freshprod_sales_grantor.hdbrole <br>
```json
{
	"role": {
		"name": "freshprod_sales#",
		"schema_roles": [{
			"names": ["freshprod_sales"]
		}]
	}
}
```

A careful glance will show us that the role name in both the `hdbrole` artifacts are the same if not for the difference of # in the grantor role. SAP HANA XSA identifies grantor roles with the use of #, think of it as a standard notation.

This is what our source project structure looks like after creating the roles:

<img src="/assets/images/sap-hana-xsa-synonyms/04-roles-in-source-app.png">
<div class="image-caption">
<b>Fig 4.</b> The new roles are placed in <b>roles</b> folder under <b>src</b> folder.
</div>

These are the only changes we have to make in the source application.

The next step is to add the service to our target application. Since, we are connecting two HDI containers. The source HDI container itself serves as the data-provider service. SAP HANA XSA provides a wizard to add database services.

<img src="/assets/images/sap-hana-xsa-synonyms/05-sap-hana-service-wizard.png">
<div class="image-caption">
<b>Fig 5.</b> We can add a service using the SAP HANA Service Connection wizard.
</div>

We can find the HDI container and select and add it. The effects of this action can be found in `mta.yaml` file.

<img src="/assets/images/sap-hana-xsa-synonyms/06-find-hdi-container.png">
<div class="image-caption">
<b>Fig 6.</b> The HDI container that serves as our data source.
</div>

The wizard the HDI container as a new resource in our `mta.yaml` configuration.

<img src="/assets/images/sap-hana-xsa-synonyms/07-mta-yaml-after-adding-service.png">
<div class="image-caption">
<b>Fig 7.</b> The HDI container service as a resource in <b>mta.yaml</b>.
</div>

The next task is to assign the roles we have previously created to the users of our **management** application in the **department** application through the service we just created. This assignment is done through a configuration file named `.hdbgrants`<sup>[4](https://help.sap.com/viewer/4505d0bdaf4948449b7f7379d24d0f0d/2.0.04/en-US/f49c1f5c72ee453788bf79f113d83bf9.html)</sup>. We have already a created `cfg` folder to store our database configuration files.

We will create `freshprod_cross_container.hdbgrants` in the `cfg` folder. Again, creating files under this specific folder structure is not mandatory but, staying organised always pays off. You will find that there are two ways to mention to the role category, `schema_roles` and `container_roles`, the latter is older notation and is supported only for backward compatibility reasons. I will advise to only use `schema_roles`. There are two ways to mention roles in the `hdbgrants` file, we can either use the `roles` or `roles_with_admin_option` keys to define them. In the case the of cross-container scenario, only the `roles` keyword can be used.

```json
{
	"XXXXXXXXX-wg92pttrbvs7can7-FreshProduceDept-FreshProduceDept-hdi-container": {
		"object_owner": {
			"schema_roles": [{
				"roles": ["freshprod_sales"]
			}]
		},

		"application_user": {
			"schema_roles": [{
				"roles": ["freshprod_sales"]
			}]
		}
	}
}
```
<img src="/assets/images/sap-hana-xsa-synonyms/08-cross-container-hdbgrants.png">
<div class="image-caption">
<b>Fig 9.</b> The <b>hdbgrants</b> file is not a database artifact and is only a config file.
</div>

The next step is to create **synonyms**. While creating synonyms, we can split the synonyms into a `.hdbsynonym` and `.hdbsynonymconfig` file. The idea is use to different synonym files, to group different synonyms or target tables, but instead of configuring each of them separately, we configure them all at in one synonym config file.

We will create a new sub-folder under the `src` folder called `synonyms` to save our `hdbsynonym` artifacts. In these files, we will only mention the name of the synonym, i.e., the alias we want to use for the target database artifact.

1. `freshproduce_sales.hdbsynonym`
```json
{
  "FRESHPRODUCE_SALES_FRUIT_SALES": {}
}
```
2. `freshproduce_details.hdbsynonym`
```json
{
	"FRESHPRODUCE_SALES_FRUIT_DETAILS": {}
}
```

Now, we can finally create a hdbsynonymconfig file in the `cfg` folder.
<img src="/assets/images/sap-hana-xsa-synonyms/10-synonym-config-cross-container.png">
<div class="image-caption">
<b>Fig 10.</b> By clicking on the object name button <b>...</b> we can access a screen that lets us select the service and table.
</div>

After adding all the tables the `freshproduce_dept.hdbsynonymconfig` file looks like this:
```json
{
  "FRESHPRODUCE_SALES_FRUIT_SALES": {
    "target": {
      "object": "FRESHPRODUCE_SALES_FRUIT_SALES",
      "schema": "FRESHPRODUCEDEPT_FRESHPRODUCEDEPT_HDI_CONTAINER",
      "database": "SYSTEMDB"
    }
  },
  "FRESHPRODUCE_SALES_FRUIT_DETAILS": {
    "target": {
      "object": "FRESHPRODUCE_SALES_FRUIT_DETAILS",
      "schema": "FRESHPRODUCEDEPT_FRESHPRODUCEDEPT_HDI_CONTAINER",
      "database": "SYSTEMDB"
    }
  }
}
```

Now we have made all the necessary changes in the target as well as the source application. We can finally build our database module and see the results.

<img src="/assets/images/sap-hana-xsa-synonyms/11-container-final-database-explorer.png">
<div class="image-caption">
<b>Fig 11.</b> The synonym is visible in the database explorer.
</div>

## References
1. [Users, Privileges, and Schemas](https://help.sap.com/viewer/4505d0bdaf4948449b7f7379d24d0f0d/2.0.05/en-US/a260b05631a24a759bba932aa6d81b64.html)
2. [Configure a Grantor for the HDI Container](https://help.sap.com/viewer/7952ef28a6914997abc01745fef1b607/2.0_SPS04/en-US/df2d69fe55e34406b1f8d54c43e6aee5.html)
3. [.hdbrole: Syntax](https://help.sap.com/viewer/3823b0f33420468ba5f1cf7f59bd6bd9/2.0.04/en-US/625d7733c30b4666b4a522d7fa68a550.html)
4. [.hdbgrants: Syntax](https://help.sap.com/viewer/4505d0bdaf4948449b7f7379d24d0f0d/2.0.04/en-US/f49c1f5c72ee453788bf79f113d83bf9.html)
