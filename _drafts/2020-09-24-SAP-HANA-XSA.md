---
layout: post
title: Breaking out of your container
author: Tejas Sanap
---
There are three ways of deploying applications in SAP HANA:
1. **Integrated Application**: ABAP API + CDS + OData + Fiori
2. **XS Classic**: Deprecated
3. **XS Advanced**: Latest and greatest

The “integrated application” approach is one of the most convenient and simple ways of creating applications with SAP HANA. We can write backend APIs in ABAP that leverage CDS views to collect and process data. This data is, then, exposed as an OData service to a Fiori application that acts as UI. However, this approach as numerous drawbacks, as well:
1. For firsts, these approach lacks the ability to use modern day application architectures that leverage **containers and microservices**, which form the foundation of any cloud-based application. “Cloud” is the future and it is inevitable that eventually all our applications will be running on some form of cloud platform.
2. We may be relying on HANA for data collection and aggregation through CDS views, some form of business logic must be coded in, which always have to be in ABAP. This **language lock-in** has been a major drawback. This is called polyglot application development.
3. **Security and access** to various kinds of data, cannot be configured on a granular level in the “integrated application” approach.

The ABAP runtime serves as a application server where business and procedural logic can be executed. However, the ABAP runtime is separate from the HANA database. Thus, SAP provided something called HANA XS. This was a small JavaScript runtime directly embedded in the HANA database, that allowed us to write business logic using JavaScript (Node.js). This is what SAP, now, calls XS Classic.

SAP HANA **XSA** stands for *XS Advanced* and though, it is the next iteration of XS Classic, significant changes have been made under the hood at the application server layer that introduce a new development model. All the above-mentioned drawbacks have been resolved in the SAP HANA XSA.

One of the core concepts of HANA XSA, is that of an HDI container. HDI, stands for *HANA Deployment Infrastructure*. Containers are built from scratch, as and when, required and deployed to the target platform.

This article is about how to access database objects, that reside outside of your application-specific container.

## General layout of any HDI container

Sending or receiving data across any HDI container requires three things: users, roles and synonyms, to be cofigured in a specific manner across both the source and target containers, for things to work out smoothly [1].

Within any container there are three kind of users:
1. Schema owner
2. Object owner
3. Application user

Roles allow us to have a fine control over which users have access to which objects and what privileges they will have. We can assign each role seperately to each kind of user. These roles are granted to each kind of users at runtime.

Any data that an application can be in three places: the ego container itself, another external HDI container or an external remote schema. Accessing data within one's ego container does not require any special efforts. However, for database objects outside one's ego container, we must create a link between the two containers, or the ego container and the external schema. 

This link is created with the help of synonyms and grantor services. The representation of the external database object in the ego container, is called a synonym. A synonym is an alias to the external database object.

## References
1. [Users, Privileges, and Schemas](https://help.sap.com/viewer/4505d0bdaf4948449b7f7379d24d0f0d/2.0.05/en-US/a260b05631a24a759bba932aa6d81b64.html)
