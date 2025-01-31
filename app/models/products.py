from uuid import UUID

from sqlalchemy import UUID, Boolean, Integer, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .sys_base import SysBase


class Products(SysBase):
    """
    Represents a product in the sales system.

    This SQLAlchemy model stores products, including their metadata, pricing settings, and relationships with other entities such as account products and product list items.

    ivars:
        id: The primary key of the product.
        :vartype id: int
        uuid: Unique identifier for the product, generated by the database.
        :vartype uuid: UUID
        name: The name of the product.
        :vartype name: str
        code: Unique code for the product, if applicable.
        :vartype code: str, optional
        terms: The terms of the product, if applicable.
        :vartype terms: str, optional
        description: A description of the product, if applicable.
        :vartype description: str, optional
        sys_allowed_price_increase: Flag indicating if a price increase is allowed at the system level.
        :vartype sys_allowed_price_increase: bool
        sys_allowed_price_decrease: Flag indicating if a price decrease is allowed at the system level.
        :vartype sys_allowed_price_decrease: bool
        man_allowed_price_increase: Flag indicating if a price increase is allowed at the manufacturer level.
        :vartype man_allowed_price_increase: bool
        man_allowed_price_decrease: Flag indicating if a price decrease is allowed at the manufacturer level.
        :vartype man_allowed_price_decrease: bool
        account_products: Relationship to the `AccountProducts` model, representing the products associated with specific accounts.
        :vartype account_products: list of AccountProducts
        product_lists_items: Relationship to the `ProductListItems` model, representing the product items within product lists.
        :vartype product_lists_items: list of ProductListItems
    """

    __tablename__ = "pm_products"
    __table_args__ = {"schema": "sales"}

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, nullable=False, autoincrement=True
    )
    uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
        unique=True,
        server_default=text("gen_random_uuid()"),
    )

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=True)
    terms: Mapped[str] = mapped_column(String(50), nullable=True)
    description: Mapped[str] = mapped_column(String(325), nullable=True)

    # global scope
    sys_allowed_price_increase: Mapped[bool] = mapped_column(
        Boolean, server_default=text("False"), nullable=False
    )
    sys_allowed_price_decrease: Mapped[bool] = mapped_column(
        Boolean, server_default=text("False"), nullable=False
    )
    man_allowed_price_increase: Mapped[bool] = mapped_column(
        Boolean, server_default=text("False"), nullable=False
    )
    man_allowed_price_decrease: Mapped[bool] = mapped_column(
        Boolean, server_default=text("False"), nullable=False
    )

    # Child relationships
    account_products = relationship("AccountProducts", back_populates="product")
    product_lists_items = relationship("ProductListItems", back_populates="product")
