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
2. We may be relying on HANA for data collection and aggregation through CDS views, some form of business logic must be coded in, which always have to be in ABAP. This **language lock-in** has been a major drawback.
3. **Security and access** to various kinds of data, cannot be configured on a granular level in the “integrated application” approach.

The ABAP runtime serves as a application server where business and procedural logic can be executed. However, the ABAP runtime is separate from the HANA database. Thus, SAP provided something called HANA XS. This was a small JavaScript runtime directly embedded in the HANA database, that allowed us to write business logic using JavaScript (Node.js). This is what SAP, now, calls XS Classic.

SAP HANA **XSA** stands for *XS Advanced* and though, it is the next iteration of XS Classic, significant changes have been made under the hood at the application server layer that introduce a new development model. All the above-mentioned drawbacks have been resolved in the SAP HANA XSA.

One of the core concepts of HANA XSA, is that of an HDI container. HDI, stands for *HANA Deployment Infrastructure*. Containers are built from scratch, as and when, required and deployed to the target platform.

This article is about how to access database objects, that reside outside of your application-specific container.
