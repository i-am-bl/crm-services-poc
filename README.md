# crm-services-poc

## Table of Contents

- [crm-services-poc](#crm-services-poc)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
    - [Purpose](#purpose)
    - [Technologies](#technologies)
    - [User Flow](#user-flow)
  - [Important: Installation Dependencies](#important-installation-dependencies)
    - [Environment Variables](#environment-variables)
      - [Setting Environment Variables](#setting-environment-variables)
    - [Docker Installation](#docker-installation)
      - [Why use Docker?](#why-use-docker)
      - [Docker Commands](#docker-commands)
    - [Connecting to Postgres Locally](#connecting-to-postgres-locally)
  - [Problem Brief](#problem-brief)
    - [What is a Customer Relationship Management System (CRM)?](#what-is-a-customer-relationship-management-system-crm)
    - [Background](#background)
    - [Problem](#problem)
      - [Currently](#currently)
      - [Desired](#desired)
    - [Objectives](#objectives)
    - [Personas](#personas)
    - [Stakeholders](#stakeholders)
    - [Industry](#industry)
  - [Solution](#solution)
    - [Vision of Scope](#vision-of-scope)
    - [High-Level Stories](#high-level-stories)
    - [KPIs (Key Performance Indicators)](#kpis-key-performance-indicators)
    - [Acceptance Criteria](#acceptance-criteria)
  - [Implementation: POC Explained](#implementation-poc-explained)
    - [Authentication](#authentication)
    - [Routers (Path Operations)](#routers-path-operations)
    - [Schemas](#schemas)
    - [Services](#services)
    - [Models](#models)
    - [Utilities](#utilities)
    - [Constants](#constants)
    - [Exception Handling](#exception-handling)
    - [Registration](#registration)
      - [Router Registration](#router-registration)
      - [Exception Handler Registration](#exception-handler-registration)
  - [APIs](#apis)
    - [Sign-up](#sign-up)
    - [Login](#login)
    - [Users](#users)
    - [Entities](#entities)
    - [Entity-Addresses](#entity-addresses)
    - [Entity-Emails](#entity-emails)
    - [Entity-Numbers](#entity-numbers)
    - [Entity-Websites](#entity-websites)
    - [Entity-Accounts](#entity-accounts)
    - [Accounts](#accounts)
    - [Account-Entities](#account-entities)
    - [Account-Addresses](#account-addresses)
    - [Account-Contracts](#account-contracts)
    - [Account-Lists](#account-lists)
    - [Account-Products](#account-products)
    - [Products](#products)
    - [Product-Lists](#product-lists)
    - [Product-Lists-Items](#product-lists-items)
    - [Orders](#orders)
    - [Order-Items](#order-items)
    - [Invoices](#invoices)
    - [Invoice-Items](#invoice-items)
  - [Conclusion](#conclusion)

## Introduction

### Purpose

It is intended to demonstrate technical acumen with various technologies that include Python, PostgreSQL, and Docker. This project is primarily focused on APIs, data flow, and the enforcing of data integrity. Data models exclude indexing and foreign key constraints at the data model layer to simplify the demonstration and interaction with the APIs. Primarily focusing on APIs, front-end development was excluded.

This project originates from first-hand experience with Customer Relationship Management (CRM) tools. Experience includes the personas of managing pricing models for client lifecycles as a product manager, billing products or services for products or services extended, and retroactively analyzing the data produced for actionable insights.

CRM tools used offered both rigid and flexible solutions. Experience with the pitfalls of both was a driver for the following ideation. Ideation includes solutions implemented and additional ideation for a more flexible construct.

### Technologies

The following highlights the technologies applied. Each was selected for an attribute to demonstrate the contextual knowledge of capabilities offered.

- **Python**:\
  This project is written in Python. Chosen for ease of use, readability, and access to the FastAPI framework.
- **FastAPI**:\
  An API python framework. Chosen for the asynchronous programming support, type safety, performance capabilities, and automatic documentation. Asynchronous non-blocking I/O is extremely efficient for interacting with the database layer, decreasing client wait times.
- **PostgreSQL**:\
  RDBMS (Relational Database Management System) technology, chosen for the feature rich dialect of SQL. It is an open-source solution that has well established branch and reputation in the market. Software defects are resolved quicker than other open-source solutions.
- **Docker**:\
  Chosen to provide a consistent environment for running the code.

### User Flow

This project is described comprehensively throughout this README, the following diagram is intended to visualize the information described. The simple flow shows the application at a high-level and provided a happy-path flow.

> Tip: Using text editors like vs code, right click and choose `show in browser` to view this html file.

- crm-user-flow: `./app/docs/crm-user-flow.html`

## Important: Installation Dependencies

### Environment Variables

#### Setting Environment Variables

- Create a `.env` file in the root directory, then copy and paste the following variables into the file.
  > **Tip**: root directory is referred to as the directory containing Docker-related files, etc.
- Create a `JWT_SECRET_KEY`.
  > This can be achieved with the following command in the terminal: `openssl rand -hex 32`. This requires python installation.

**Environment Variables**:
The following environment variables are essential for successful code build.

```python
# Database specific variables, essential for creating a successful connection string.
DB_CONNECTOR=postgresql+asyncpg   # driver for database connection string
DB_USRNM=postgres                 # database username, this is the default root user for PostgreSQL
DB_PWD=****                       # database password, '****' is not a valid password, this is a placeholder
DB_HST=postgres-db                # database host, specified in docker-related files
DB_PORT=5432                      # database port number, specified in docker-related files
DB_NM=tech                        # database name

# JWT specific variables
JWT_SECRET_KEY=                   # secret key for encoding JWT
JWT_ALGORITHM=                    # algorithm for encoding JWT, example: JWT_ALGORITHM=HS256
JWT_EXPIRATION=                   # expiration in minutes, example: JWT_EXPIRATION=15

```

---

### Docker Installation

This project was developed in Docker. If you do not have Docker installed locally or if you have not used Docker before, please refer to the following link.

[Install Docker](https://docs.docker.com/engine/install/)

> **Tip**: The installation guide will help make the installation process seamless.

#### Why use Docker?

Using Docker helps maintain a consistent development environment, ensuring that all users will have the same experience.

#### Docker Commands

- **Start Containers**: `docker-compose up -d`\
  Starts the containers in detached mode, allowing the containers to run in the background without running any specified commands in the Dockerfile.
- **Build Image and Start Containers**: `docker-compose up --build`\
  Forces a build of the images and runs the commands specified in the `Dockerfile`.
- **Stop Containers**:\
  Press `ctrl+c` to disrupt a current process to return to the terminal.
- **Shut Down Containers**: `docker-compose down`\
  Stops and removes the containers when done.

### Connecting to Postgres Locally

To connect to the Postgres instance hosted in Docker, use your preferred database management tool.

> **Tip**: Port must be set to **5445**, not **5432**, for a successful connection. The Postgres instance was exposed externally for connections outside of the Docker network on a different port to avoid conflict for any pre-existing local Postgres instances.

---

## Problem Brief

### What is a Customer Relationship Management System (CRM)?

A CRM (Customer Relationship Management System) is a business tool that manages interactions with clients. It centralizes client information and streamlines processes to improve communication between departments.

CRMs come in many flavors; some key features are listed below.

- Contact Management
- Sales Tracking
- Customer Service
- Marketing Automation
- Analytical and Reporting
- Product and Pricing Management
- Account Management
- Ordering and Invoicing

> **Please Note:** Project concentrates on product and pricing management, account management, and ordering and invoicing.

### Background

SMBs (Small and Medium-Sized Business) do not always follow a consistent pricing strategy. Smaller businesses participate in relationship selling. Relationship selling authorizes a sales consultant to close the deal at the cost of all profit margin, creating inconsistent contract agreement terms. It is difficult to manage with a few clients, impossible with several clients. This effectively produces a high closure rate for sales, however; post closure management of contract terms can be difficult for supporting teams that include operations, product, and client success.

Choosing the right CRM software is daunting. Business models vary across industries and CRMs are designed to be generalized, highlighting a few key attributes, or extending unimagined flexibility. Flexiblity is powerful, but requirements gathering, and a vision is required to customize to meet business needs. Some solutions require certain technical skills to effectively implement.

### Problem

The business has grown, adding clients and team members. Responsibilities were centralized, focusing teams to increase productivity. Operational productivity was increased but communication between departments declined. Billing became a nightmare that was unmanageable.

#### Currently

Contracts are automatically renewed without review, services provided are not properly billed, and unapproved discounts are applied. Recurring billing is not always being billed. Services are being performed that were not ordered or not under contract.

Products are allowed one price for all clients. Contracts specify a variation in discount models from list price per client.

#### Desired

To effectively enforce pricing strategy, more transparency into the account lifecyle must be readily accessible through data. If this data could be queried from a database, it would be highly beneficial. Examples of required insight include varying pricing structures, products or services explicitly excluded from a master service agreement, condition length, and agreement length.

It is desired to retain the historical pricing structures for a product. Insight into the original price and the billed price is required by product per client. Increased restriction on price adjustments such as price increases or decreases are needed to enforce approved pricing.

### Objectives

- Retain historical pricing information to provide actionable insights into pricing strategy.
- Implement more control for allowed price adjustment per product (global scope) and price list (local scope).
- Store relevant contract information facilitate client relationship monitoring.

---

### Personas

- **Product Manager**:\
  Directly manages price books and pricing strategies. Interactions in a CRM includes managing products, pricing, price books, assignment of price books to clients, and analyzing historical sales data.
- **Client Success Manager**:\
  Directly interacts with the client, manages contract lifecycles. Interaction in CRM includes account and contract review, account creation and setup.
- **Operations**: \
  Producer of services extended to clients. Interactions in CRM include the creation of sales orders, billing services, approving sales orders, and reviewing account information.

---

### Stakeholders

- **Chief Operating Officer**:\
  Oversees operations and day-to-day activities of production.
- **Product Director**:\
  Oversees product and pricing strategies.
- **Client Success Manager**:\
  First line communication with clients.

### Industry

Industry is generalized and client base is generalized in the scope of this problem

---

## Solution

### Vision of Scope

Implement a solution that will mitigate business risk that has stemmed from pricing variation and the decline in departmental communication.

### High-Level Stories

As a Product Manager, I want to establish a standard price list that can be associated with client accounts. I do not want to create custom price books unless there is pricing variation. This will simplify price book management if clients opt to exclude products or services. It is extremely important to accecss historical pricing data to retroactively identify actionable insight for future pricing strategies.

As a Client Success Manager, I want to effectively manage the contract lifecycle for clients, providing a better client experience.

As an Operation Manager, I want to safeguard my staff from creating billing errors. I wish products and prices were established for the acount serviced and the staff can simply create an order for the service provided.

### KPIs (Key Performance Indicators)

- Instances of incorrect billing.
- Instances of missed contract renewal dates.

### Acceptance Criteria

- Historical pricing information is retained.
- Products and services under contractual agreement can be accessed with database queries.
- Pricing can be configured per client to have multiple prices.

## Implementation: POC Explained

Section highlights key attributes implemented to explain the design concepts and the benefits provided.

> **Please Note**: Authorization was out of scope for this project. It was excluded to simplify the complexity of the deomonstration.

The below table provides a summary of the implemented layers.

| Layer          | Description                                   |
| -------------- | --------------------------------------------- |
| Authentication | Authentication with JWT.                      |
| Routes         | API endpoints or path operations.             |
| Schemas        | Data validation layer.                        |
| Services       | Business logic layer.                         |
| Models         | Data model layer.                             |
| Database       | Database operations and connection layer.     |
| Utilities      | Reusable code.                                |
| Constants      | Constant files.                               |
| Exceptions     | Custom exception handling.                    |
| Registration   | Registering routers and handlers dynamically. |

### Authentication

Authentication was implemented with the use of a JWT (JSON Web Token) and stored as a cookie. Due to the limited scope of this demonstration, a refresh or blacklist process of a JWT was not implemented. Token is set to expire by specified duration, set in the environment variable layer. If not specified, expiration defaults to 15 minutes. To supplement a refresh process, each path operation validates the existence of a valid token; if valid, a new token is issued.

Implentation include a combination of a decorator and a dependency found in each path operation.

The below is an example for a path operation that incldues the dependency and decorator.

```python
@router.get(
    "/{account_uuid}/addresses/{address_uuid}/",
    response_model=s_addresses.AddressesResponse,
    status_code=status.HTTP_200_OK,
    include_in_schema=False,
)
@serv_token.set_auth_cookie  # Decorator sets new issued JWT as a cookie
@handle_exceptions([AddressNotExist])
async def get_address(
    response: Response,
    account_uuid: UUID4,
    address_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple = Depends(serv_session.validate_session),  # Validates JWT, returns tuple of (sys_user, new token)
) -> s_addresses.AddressesResponse:
    """get one address"""
```

---

### Routers (Path Operations)

FastAPI, an API framework, was leveraged to implement asynchronous I/O (Input/Output) operations. Path operations have dedicated routers, abstracting operations to distinctly dedicated files for clear separation of concerns. Business logic is handled in the [service layer](#services). When cross-functional service calls are required, it was implemented in the router layer.

```python
# All pathe operations are decorated with a @router
@router.get(
    "/{account_uuid}/addresses/{address_uuid}/",    # path
    response_model=s_addresses.AddressesResponse,   # response schema, also appears in OpenAPI docs
    status_code=status.HTTP_200_OK,                 # response status code
    include_in_schema=False,
)
@serv_token.set_auth_cookie
@handle_exceptions([AddressNotExist])
async def get_address(
    response: Response,
    account_uuid: UUID4,
    address_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple = Depends(serv_session.validate_session),
) -> s_addresses.AddressesResponse:
    """get one address"""
```

---

### Schemas

Pydantic, a data validation library, was leveraged to enforce data integrity and to possess more control over data exchanged between client and server. Schemas are abstracted from the data model layer but foundationally mirror data models. At the foundation, multiple schemas have been implemented to enforce data requrirements for the allowed exchange or modification of data.

Extending from the foundation, schemas in the primary context include combinations of multiple models for more complex data exchange between client and server. These schemas typically extend from the base schemas.

Request bodies do not require all fields to be sent. The schema layers include explicit and optional exclusion. Optional values default to `None` or an explicit value for fields that are `Not Nullable`.

Update or `PUT` operations behave as a `PATCH` compared to traditional replace behavior. If an optional field is excluded, original value is retained if exists. Updating a `Nullabe` field to `Null` is supported, achievable by passing `""` or empty string. `Null` values are explicitly excluded at the service layer but empty strings are recognized, translated to `Null` and passed to the data layer.

All `sys_fields` are system generated by either application code or the server defaults at the data model layer.

Schema models are designed to directly map to the data models. More complex queries have specific schema that mirror the label specified in query statement layer than directly translating to the data model.

```python

# Example of direct mapping to data model
class Entities(BaseModel):
    type: Annotated[
        EntityTypes,
        Literal[EntityTypes.ENTITY_INDIVIDUAL, EntityTypes.ENTITY_NON_INDIVIDUAL],
    ]

# Example of schema mapping to query statement
class EntitiesIndivNonIndivResponse(BaseModel):
    entity_uuid: Optional[UUID4] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    company_name: Optional[str] = None

    class Config:
        from_attributes = True

# Example of combined responses
class EntitiesCombinedResponse(BaseModel):
    entity: Optional[EntitiesResponse] = None
    individual: Optional[IndividualsResponse] = None
    non_individual: Optional[NonIndividualsResponse] = None

```

---

### Services

Microservice design limits the scope of each service to interact with a specific data model for seperation of concerns. Files can be found in `./services`. Business logic for database interaction lives at the service layer. Cross functional service calls are supported, abstracted to the [path operation](#routers-path-operations) layer if required.

Need for cross functional service calls were limited, additional abstraction was not needed at this time.

Service layer seperates SQL queries for interacting with the data layer and operations such as create, read, update, and delete. Contract is enforced with inner classes.

Clear seperation extends flexibility for cross functional service use.

> **Example:** Read operation is indirectly used for record existence validation prior to creation. The soft delete design limits contraints at the data layer.

The below example includes the `Entities Read Service`. Queries, database operations, validation checks have been abstracted.

```python
class EntitiesServices:
    pass

    class ReadService:
        def __init__(self) -> None:
            pass

        async def get_entity(
            self, entity_uuid: UUID4, db: AsyncSession = Depends(get_db)
        ):
            statement = EntitiesStatements.SelStatements.sel_entity(              # Database query
                entity_uuid=entity_uuid
            )
            entity = await Operations.return_one_row(                             # Database Operation
                service=cnst.ENTITIES_READ_SERV, statement=statement, db=db
            )
            return di.record_not_exist(instance=entity, exception=EntityNotExist) # Data validation and exception handling
```

---

### Models

SQL Alchemy, an ORM (Object Relationship Mapping), was leverage for database interation. In `./models`, each file consists of a data model or database table. Through inheritence, an abstract class efficiently distributes fields that were designed to exist on every table. Fields incldude sys_fields for capturing a reference to a user that took a write action on the record and time of action.

Concept of soft deletes were incorporated into the data design, preserving referential integrity. Soft deleted records are filtered at the API level.

```python
# Example of data models with inheritence, SysBase is a custom abstract class
class Entities(SysBase):
    __tablename__ = "em_entities"  # tables have been prefixed will module identifier to group relevant tables
    __table_args__ = (
        CheckConstraint(
            "type in ('individual', 'non-individual')", name="entities_type_check"
        ),
        {"schema": "sales"},
    )

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, nullable=False, autoincrement=True
    )
    uuid: Mapped[uuid4] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
        server_default=text("gen_random_uuid()"),
        unique=True,
    )

    entity_types = ["individual", "non-individual"]
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    tin: Mapped[str] = mapped_column(String(20), nullable=True)

```

```sql
-- Comparison to generated DDL (Data Definition Language)
-- sales.em_entities definition

CREATE TABLE sales.em_entities (
    id serial4 NOT NULL,
    "uuid" uuid DEFAULT gen_random_uuid() NOT NULL,
    "type" varchar(50) NOT NULL,
    tin varchar(20) NULL,
    sys_created_at timestamptz DEFAULT now() NOT NULL,
    sys_created_by uuid NULL,
    sys_updated_at timestamptz NULL,
    sys_updated_by uuid NULL,
    sys_deleted_at timestamptz NULL,
    sys_deleted_by uuid NULL,
    CONSTRAINT em_entities_pkey PRIMARY KEY (id),
    CONSTRAINT em_entities_uuid_key UNIQUE (uuid),
    CONSTRAINT entities_type_check CHECK (((type)::text = ANY ((ARRAY['individual'::character varying, 'non-individual'::character varying])::text[])))
);**

```

---

### Utilities

Various utilities were created to mitigate risk of code duplication.

---

### Constants

Constants include static messages, globally constant variables, error codes, and configuration JSONs for dynamic configuration of routers and exception handlers.

---

### Exception Handling

Custom exception claseses were established for custom messaging, logging, and to possess more control over the error. Limited logging and exception handling was implemented for simplicity. Established pattern is designed for extension. Data validation utilities pass exceptions as parameters, raising custom exception.

Custom Exception class include custom logging. Solution is open to extension for additional params or message modification.

```python
# Custom Exception class
# Class inherits custom logger from CRMException base class that will log message passed
class AccContractExists(CRMExceptions):
    def __init__(
        self, message: str = ACCCOUNT_CONTRACT_EXISTS, *args: object, **kwargs
    ) -> None:
        super().__init__(message, *args, **kwargs)

# Service
class CreateService:
    def __init__(self) -> None:
        pass

    async def create_account_contract(
        self,
        account_uuid: UUID4,
        account_contract_data: s_account_contracts.AccountContractsCreate,
        db: AsyncSession = Depends(get_db),
    ):
        account_contracts = AccContractsModels.account_contracts
        account_contract = await Operations.add_instance(
            service=cnst.ACCOUNTS_CONTRACTS_CREATE_SERVICE,
            model=account_contracts,
            data=account_contract_data,
            db=db,
        )
        return di.record_not_exist(
            instance=account_contract, exception=AccContractNotExist # exception is passed as param
        )

# data validation utility, exception is passed, raised an then name is logged.
@classmethod
def record_not_exist(cls, instance: object, exception: Exception) -> bool:
    if not instance:
        class_name = exception.__name__
        logger.warning(f"Warning: record not found for {class_name}")
        raise exception() # exception is raised
    return instance
```

Example of the decoraor that wraps path operations.

```python
@router.get(
    "/{account_uuid}/account-contracts/{account_contract_uuid}/",
    response_model=s_account_contracts.AccountContractsReponse,
    status_code=status.HTTP_200_OK,
    include_in_schema=False,
)
@serv_token.set_auth_cookie
@handle_exceptions([AccContractNotExist])   # Decorator recieves exception classes as a list
async def get_account_contract(
    response: Response,
    account_uuid: UUID4,
    account_contract_uuid: UUID4,
    db: AsyncSession = Depends(get_db),
    user_token: Tuple = Depends(serv_session.validate_session),
) -> s_account_contracts.AccountContractsReponse:
    """get one account contract"""

    async with transaction_manager(db=db):
        return await serv_acc_contr_r.get_account_contract(
            account_uuid=account_uuid,
            account_contract_uuid=account_contract_uuid,
            db=db,
        )

```

Custom exception classes are complimented with a decorator that takes anticipated exceptions as a list, to re-raise the original exception, maintaining the integrity of the original traceback. Decorator wraps path operation with a try, except block.

```python
def handle_exceptions(exception_classe: List[Type[Exception]]):
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except tuple(exception_classe):
                raise
            except SysUserNotExist:
                raise
            except Exception as e:
                raise UnhandledException

        return wrapper

    return decorator
```

### Registration

#### Router Registration

Abstracting routers to individual files requires registration. Registration was achieved by exporting routers as a module, creation of an router registration handler, and a configuration file.

**Configuration file**:
The configuration file is passed to the handler as a param. This configuration file also abstracts the documentation logic FastAPI offers for the creation of OpenAPI docs from the pathe operation level to this file.

```python

"""
Name and allow_registration are custom.
name: for logging purposes
allow_registration: boolean controls if router will be registered

The other items are FastAPI specific can be found in their documentation.
"""

routers = {
    "routers": [
        {
            "name": "api_doc_router",
            "router": api_doc_router,
            "prefix": "",
            "tags": [cnst.TAG_SIGN_UP],
            "dependencies": None,
            "responses": None,
            "deprecated": False,
            "include_in_schema": True,
            "default_response_class": HTMLResponse,
            "callbacks": None,
            "generate_unique_id": generate_unique_id,
            "allow_registration": True,
        },
    ]
}

```

#### Exception Handler Registration

**Configuration File**:
The configuration file is passed to the exception registration handler fucntion as a param.

```python
handlers = {
    "account_contracts": [
        {
            "class": AccContractNotExist,
            "error_code": err.ACCCOUNT_CONTRACT_NOT_EXIST,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": msg.ACCCOUNT_CONTRACT_NOT_EXIST,
            "allow_registration": True,
        },
        {
            "class": AccContractExists,
            "error_code": err.ACCCOUNT_CONTRACT_EXISTS,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": msg.ACCCOUNT_CONTRACT_EXISTS,
            "allow_registration": True,
        },
    ],
}
```

FastAPI allows for Exception registration through creation of specific handlers. One handler was created that returned a reusble handler dynamically for a more efficient approach. This appoach provides a templated approach to handling exceptions.

```python
def create_exception_handler(
    status_code: int,
    error_code: str,
    message: Any,
) -> Callable[[Request, Exception], JSONResponse]:

    async def exception_handler(request: Request, exec: CRMExceptions):
        return JSONResponse(
            status_code=status_code,
            content={"error_code": error_code, "message": message},
        )

    return exception_handler
```

---

## APIs

Interactive and detailed information for path operations are generated at `/docs` and `/redoc`. The below sections describe the API, providing business context.

> **Tip**: The described pathing for OpenAPI documentation is intended to be appended to `localhost:8000` in a browser if code is ran.

### Sign-up

For demo purposes only. This provides a self-sign up experience.

### Login

Login operation validates the credentials, issuing a JWT as a cookie upon successful credential validation.

### Users

System users of the application. No two active users can have the same email and/or username.

### Entities

Entities incldue individuals and non-individuals. It is the foundational of the application.

| type           | first_name | last_name | company_name  |
| -------------- | ---------- | --------- | ------------- |
| individual     | tom        | johnson   |               |
| non-individual |            |           | business name |

### Entity-Addresses

Addresses are stored as a list, extending flexibility for storing multiple addresses.

> **Example**: Physical Address, Mailing Address, Billing Address, etc.

| type     | address_line1 | address_line2 | city       | county       | state    | zip   | country       |
| -------- | ------------- | ------------- | ---------- | ------------ | -------- | ----- | ------------- |
| physical | 134 lane      | building 1    | smallville | small county | michigan | 78491 | united states |
| mailing  | 134 lane      | building 1    | smallville | small county | michigan | 78491 | united states |

### Entity-Emails

Emails are stored as a list, extending flexibility for storing many types of emails.

| type | email                       | description      |
| ---- | --------------------------- | ---------------- |
| work | <tom.johnson@email.com>     | business 1 email |
| work | <tom.johnson123@email.com>  | business 2 email |
| work | <tom.johnson1234@email.com> | business 3 email |

### Entity-Numbers

Phone numbers are stored in list format, extending flexibility for tracking many methods of contact information.

| type        | number     |
| ----------- | ---------- |
| primary     | 1.614.8888 |
| direct line | 1.555.8888 |
| work line   | 1.444.8888 |

### Entity-Websites

Website URLs are stored in a list format, extending flexibility for storing many websites per entity.

| type      | url                                     | description |
| --------- | --------------------------------------- | ----------- |
| corporate | <https://wwww.corporate.business.org/>  | business 1  |
| corporate | <https://wwww.corporate2.business.org/> | business 2  |

### Entity-Accounts

Relationship between an [entity](#entities) and an [account](#accounts). Accounts cannot exist without an entity. This extends flexibility for allowing an entity to have multile accounts.

Relationship is designed to be from the perspective of the entity.

| account_id | account_name            |
| ---------- | ----------------------- |
| 001        | account-org-1-marketing |
| 002        | account-org-2-sales     |

### Accounts

Accounts are the foundation for sales and billing clients. An entity must have an account to be billed for products or services provided. Only active account that do not have an end date can be billed.

| id  | name                    | start_on   | end_on |
| --- | ----------------------- | ---------- | ------ |
| 001 | account-org-1-marketing | 01/15/2023 |        |
| 002 | account-org-2-sales     | 05/15/2024 |        |

### Account-Entities

Account-Entities is the same relationship described in [Entity-Accounts](#entity-accounts). This is from the perspective of an account.

| name         | type           | start_on   | end_on     |
| ------------ | -------------- | ---------- | ---------- |
| business 1   | account holder | 01/15/2020 |            |
| john smith   |                | 01/15/2020 | 12/15/2022 |
| bill johnson | approver       | 01/15/2020 |            |
| chris tims   |                | 03/15/2023 |            |

### Account-Addresses

Address relationship is similar to the relationsip described in [Entity-Addresses](#entity-addresses). The information stored is similar in nature but allows for specific addresses to be linked at the account level.

| type     | address_line1 | address_line2 | city       | county       | state    | zip   | country       |
| -------- | ------------- | ------------- | ---------- | ------------ | -------- | ----- | ------------- |
| physical | 134 lane      | building 1    | smallville | small county | michigan | 78491 | united states |
| mailing  | 134 lane      | building 1    | smallville | small county | michigan | 78491 | united states |
| billing  | 134 lane      | building 1    | smallville | small county | michigan | 78491 | united states |

### Account-Contracts

Contracts are stored in a list format, extending for flexibility of tracking or storing multiple agreements for an account.

| name                     | start_on   | end_on     | notification_days |
| ------------------------ | ---------- | ---------- | ----------------- |
| master service agreement | 01/01/2022 | 12/31/2025 | 45                |
| purchase sales agreement | 01/01/2022 | 12/31/2025 | 45                |
| software sales agreement | 01/01/2022 | 12/31/2025 | 45                |

### Account-Lists

Account-Lists is a relationship between an [account](#accounts) and a [product list](#product-lists). Relationship establishes a link between the account and product list to effectively manage prices of products and services.

| product_list    | start_on   | end_on     |
| --------------- | ---------- | ---------- |
| 2024 price book | 01/01/2024 | 12/31/2024 |

### Account-Products

Account-Products is a relationship between a [product](#products) and an [account](#accounts). This is an additional layer to [account-lists](#account-lists). This layer will restrict an account to specific products, regardless of the linked product-list. Restriction will limit the account to products or services that have been contractually agreed upon.

| product   | start_on   | end_on     |
| --------- | ---------- | ---------- |
| product a | 01/01/2024 | 05/15/2024 |
| product b | 01/01/2024 |            |

### Products

Product or service offered provided to clients.

Price is not managed at the product level. Price is managed at the [product list](#product-lists) level to effectively managed various pricing models.

**Example:**

| name      | code   | terms           | description                             |
| --------- | ------ | --------------- | --------------------------------------- |
| product a | 001251 | per transaction | Description of product or service sold. |

### Product-Lists

Product lists can also be understood as price catalogs or price books. Lists are designed to be containers for products. Abstracting the price management from the product level, price variation can be effectively managed.

**Example:**

| name            | description          | effective_on | expires_on |
| --------------- | -------------------- | ------------ | ---------- |
| 2024 price book | 2024 pricing         | 01/01/2024   | 12/31/2024 |
| 2024 client a   | 2024 special pricing | 2/15/2024    | 5/15/2024  |

### Product-Lists-Items

Relationship between [products](#products) and [product lists](#product-lists). Price of a products are managed at this level to effectively manage price variance.

**Example:**

| product_list    | product   | price  |
| --------------- | --------- | ------ |
| 2024 price book | product a | $25.00 |
| 2024 client a   | product a | $23.00 |

### Orders

Orders contain billables for a product or service that must follow the approval lifecycle. This requires approval from a manager. Once approved, the billable will become read-only, generating an invoice or snapshot of the order.

**Example:**

| order_id | account_name  |
| -------- | ------------- |
| 215      | Dummy-Account |

### Order-Items

The details of the [order](#order-items). These line items can be chosen from the allowed products from [account products](#account-products) and [account lists](#account-lists).

| product_name     | quantity | price  | adjustment_type | priceadjustment | amountbilled | description |
| ---------------- | -------- | ------ | --------------- | --------------- | ------------ | ----------- |
| billable service | 3        | $25.00 | dollar          | $-2.00          | $69.00       |             |

### Invoices

A snapshot of [orders](#orders) to create a historical reference in the event modifications are needed. The invoice must be canceled and the sales order must be reopend, modified, and reapproved.

Statements are generated from invoice information.

**Example:**

| id  | order_id | status   |
| --- | -------- | -------- |
| 001 | 001      | canceled |
| 002 | 001      | paid     |

### Invoice-Items

Items are a snapshot of [order items](#order-items). Following the paradigm described in [invoices](#invoices), these items are not designed to be modified.

## Conclusion

This project was greatly simplified. It discloses real problems faced as a product manager, managing price strategy. In a product role, I have used CRMs that do not fit the needs of the business. This can make things very difficult and inefficient. With extremely flexible tools, solutions were achieved. This showcases those solutions.

The outcome saved alot of time and significantly decreased problem areas.
