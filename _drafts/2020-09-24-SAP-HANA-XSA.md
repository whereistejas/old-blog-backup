---
layout: post
title: Breaking out of your container
author: Tejas Sanap
---
There are three ways of deploying applications in SAP HANA:
1. **Integrated Application**: ABAP API + CDS + OData + Fiori
2. **XS Classic**: This has been deprecated since HANA SPS 02
3. **XS Advanced**: The latest and greatest, native HANA application

The “integrated application” approach is one of the most convenient and simple ways of creating applications with SAP HANA. We can write backend APIs in ABAP that leverage CDS views to collect and process data. This data is, then, exposed as an OData service to a Fiori application that acts as UI. However, this approach as numerous drawbacks, as well:
1. For firsts, these approach lacks the ability to use modern day application architectures that leverage **containers and microservices**, which form the foundation of any cloud-based application. “Cloud” is the future and it is inevitable that eventually all our applications will be running on some form of cloud platform.
2. We may be relying on HANA for data collection and aggregation through CDS views, some form of business logic must be coded in, which always have to be in ABAP. This **language lock-in** has been a major drawback. Being able to develop an application using multiple languages is called polyglot application development.
3. **Security and access** to various kinds of data, cannot be configured on a granular level in the “integrated application” approach.

The ABAP runtime serves as a application server where business and procedural logic can be executed. However, the ABAP runtime is separate from the HANA database. Thus, SAP provided something called HANA XS. This was a small JavaScript runtime directly embedded in the HANA database, that allowed us to write business logic using JavaScript (Node.js). This is what SAP, now, calls XS Classic.

SAP HANA **XSA** stands for *XS Advanced* and though, it is the next iteration of XS Classic, significant changes have been made under the hood at the application server layer that introduce a new development model. All the above-mentioned drawbacks have been resolved in the SAP HANA XSA.

One of the core concepts of HANA XSA, is that of an HDI container. HDI, stands for *HANA Deployment Infrastructure*. In HANA XSA, application are pushed from git repositories, by building them from source, and deploying them to the target platform, in the form of containers.

This article is about how to access database objects, that reside outside of your application-specific container, which I will call the ego container, here onwards.

## How does a container work?

Any form of cross-container or schema interaction requires three things: 
1. A mechanism that grants users with specific roles.
2. Aliases pointing towards the appropriate external database object.
3. Services that help the two entities communicate, sending information back and forth.

All of them have to be configured in a specific manner across both the source and target container/schema, for things to work out smoothly<sup>[1](https://help.sap.com/viewer/4505d0bdaf4948449b7f7379d24d0f0d/2.0.05/en-US/a260b05631a24a759bba932aa6d81b64.html)</sup> when the containers are created post-deployment during runtime.

Within any container, there are three kind of users:
1. *Schema owner*, is the user who owns/creates the ego container.
2. *Object owner*, is the user who owns all the database objects within the various schemas of the container.
3. *Application user*, is the end user who uses the application and accesses the data within the container.

Roles allow us to have a fine control over which users have access to which objects and what privileges they will have over those objects. These roles are granted to various users during runtime, whenever they use the application.

Any data that an application may need can be in three places: the ego container, another external HDI container or an external remote schema. Accessing data within the ego container does not require any special efforts. However, for any database object outside the ego container, we must create a connection between the ego container and the external HDI container or remote schema.

This connection is created with the help of synonyms and grantor services. The representation of the external database object in the ego container, is called a **synonym**. A synonym is an alias to the external database object. A **grantor service** is an user-defined service that connects the ego container to the remote database hosting the external schema artifacts<sup>[2](https://help.sap.com/viewer/7952ef28a6914997abc01745fef1b607/2.0_SPS04/en-US/df2d69fe55e34406b1f8d54c43e6aee5.html)</sup>.

In this blog post, we will cover two cross-container data scenarios:
1. Reading data from another HDI container.
2. Reading data from an external remote schema/database.

## Basic Premise

<img src="/assets/images/sap-hana-xsa-synonyms/01-project-view1.png">
<div class="image-caption">
<b>Fig 1.</b> Source and target applications.
</div>

Let's take the example of a super-market chain. The supermarket company has different applications to analyse the sales of different categories of items. So, packed food gets its own application, fresh produce gets its own application. In our case, we have the application for the department that manages fresh produce, which covers all vegetables and fruits, we will call this the **department** application.

The management uses a different application, where data from the all the departments is gathered and showed, so as to give them a birds eye view. We will call this application the **management** application.

Some of the data, that the management application needs is stored in the department application's container and some of it is stored in a remote ERP database.

Thus, the Department application is our source system and the management application is our target system.

## How to connect to another HDI container?

<img src="/assets/images/sap-hana-xsa-synonyms/02-cross-container-scenario.png" width="25%">
<div class="image-caption">
<b>Fig 2.</b> Process.
</div>

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
