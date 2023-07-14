from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.item_mydict import ItemMydict


T = TypeVar("T", bound="Item")


@attr.s(auto_attribs=True)
class Item:
    """can this item thing have any schema description?

    Attributes:
        name (str):
        price (float):
        is_offer (bool): is offer description
        my_dict (ItemMydict):
    """

    name: str
    price: float
    is_offer: bool
    my_dict: "ItemMydict"
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        price = self.price
        is_offer = self.is_offer
        my_dict = self.my_dict.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "price": price,
                "is_offer": is_offer,
                "myDict": my_dict,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.item_mydict import ItemMydict

        d = src_dict.copy()
        name = d.pop("name")

        price = d.pop("price")

        is_offer = d.pop("is_offer")

        my_dict = ItemMydict.from_dict(d.pop("myDict"))

        item = cls(
            name=name,
            price=price,
            is_offer=is_offer,
            my_dict=my_dict,
        )

        item.additional_properties = d
        return item

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
