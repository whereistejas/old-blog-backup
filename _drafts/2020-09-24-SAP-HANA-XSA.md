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

One of the core concepts of HANA XSA, is that of an HDI container. HDI, stands for *HANA Deployment Infrastructure*. In HANA XSA, application are pushed from git reppositories, by building them from source, and deploying them to the target platform, in the form of containers.

This article is about how to access database objects, that reside outside of your application-specific container, which I will call the ego container, here onwards.

## How does a container work?

Any form of cross-container or schema interaction requires three things: 
1. A mechanism that grants users with specific roles.
2. Aliases pointing towards the appropriate external database object.
3. Services that help the two entities communicate, sending information back and forth.

All of them have to be cofigured in a specific manner across both the source and target container/schema, for things to work out smoothly<sup>[1](https://help.sap.com/viewer/4505d0bdaf4948449b7f7379d24d0f0d/2.0.05/en-US/a260b05631a24a759bba932aa6d81b64.html)</sup> when the containers are created post-deployment during runtime.

Within any container, there are three kind of users:
1. *Schema owner*, is the user who owns/creates the ego container.
2. *Object owner*, is the user who owns all the database objects within the various schemas of the container.
3. *Application user*, is the end user who uses the application and accesses the data within the container.

Roles allow us to have a fine control over which users have access to which objects and what privileges they will have over those objects. These roles are granted to various users during runtime, whenever they use the application.

Any data that an application may need can be in three places: the ego container, another external HDI container or an external remote schema. Accessing data within the ego container does not require any special efforts. However, for any database object outside the ego container, we must create a connection between the ego container and the external HDI container or remote schema.

This connection is created with the help of synonyms and grantor services. The representation of the external database object in the ego container, is called a **synonym**. A synonym is an alias to the external database object. A **grantor service** is an user-defined service that connects the ego container to the remote database hosting the external schema artifacts<sup>[2](https://help.sap.com/viewer/7952ef28a6914997abc01745fef1b607/2.0_SPS04/en-US/df2d69fe55e34406b1f8d54c43e6aee5.html)</sup>.

In this blogpost, we will cover two cross-container data scenarios:
1. Reading data from another HDI container.
2. Reading data from an external remote schema/database.

## Basic Premise

<img src="/assets/images/sap-hana-xsa-synonyms/project-view1.png">
<div class="image-caption">
<b>Fig 1.</b> Source and target applications
</div>

Let's take the example of a super-market chain. The supermarket company has different applications to analyse the sales of different categories of items. So, packed food gets its own application, fresh produce gets its own application. In our case, we have the application for the department that manages fresh produce, which covers all vegetables and fruits, we will call this the **department** application.

The management uses a different application, where data from the all the departments is gathered and showed, so as to give them a birds eye view. We will call this application the **management** application.

Some of the data, that the management application needs is stored in the department application's container and some of it is stored in a remote ERP database.

Thus, the Department application is our source system and the management application is our target system.

## How to connect to another HDI container?

<img src="/assets/images/sap-hana-xsa-synonyms/cross-container-scenario.png" width="25%">
<div class="image-caption">
<b>Fig 2.</b> Process
</div>

To enable cross container access is create roles that give us access to the data we need. This is done using a HANA database artifact of `.hdbrole` type.

I have created a new HANA database module in our source system with the following folder structure. There is no hard and fast requirement over the folder structure, but being organised always pays off.

<img src="/assets/images/sap-hana-xsa-synonyms/source-project-structure.png">
<div class="image-caption">
<b>Fig 3.</b> Source application/Department application structure and data model.
</div>

We will be creating two `.hdbrole` artifacts. One for the schema owner and another for the application user:
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
		"object_privileges": [{
			"name": "FRESHPRODUCE_SALES_FRUIT_DETAILS",
			"type": "TABLE",
			"privileges_with_grant_option": ["SELECT"]
		}, {
			"name": "FRESHPRODUCE_SALES_FRUIT_SALES",
			"type": "TABLE",
			"privileges_with_grant_option": ["SELECT"]
		}]
	}
}
```

## References
1. [Users, Privileges, and Schemas](https://help.sap.com/viewer/4505d0bdaf4948449b7f7379d24d0f0d/2.0.05/en-US/a260b05631a24a759bba932aa6d81b64.html)
2. [Configure a Grantor for the HDI Container](https://help.sap.com/viewer/7952ef28a6914997abc01745fef1b607/2.0_SPS04/en-US/df2d69fe55e34406b1f8d54c43e6aee5.html)
