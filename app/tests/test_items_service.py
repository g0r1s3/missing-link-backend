from app.schemas.item import ItemCreate
from app.services import items as service

def test_create_and_get_item():
    created = service.create_item(ItemCreate(name="Pumpe", description="Mini"))
    fetched = service.get_item(created.id)
    assert fetched is not None
    assert fetched.name == "Pumpe"
    assert fetched.description == "Mini"

def test_list_items_filter_and_pagination():
    # Arrange
    service.create_item(ItemCreate(name="Pumpe A"))
    service.create_item(ItemCreate(name="Schlauch"))
    service.create_item(ItemCreate(name="Pumpe B"))

    # Filter: nur "Pumpe"
    filtered = service.list_items(q="pum")
    assert len(filtered) == 2

    # Pagination: limit/offset
    all_items = service.list_items()
    assert len(all_items) == 3
    assert len(service.list_items(limit=1, offset=0)) == 1
    assert len(service.list_items(limit=1, offset=1)) == 1

def test_update_and_delete_item():
    created = service.create_item(ItemCreate(name="Alt"))
    updated = service.update_item(created.id, ItemCreate(name="Neu"))
    assert updated is not None
    assert updated.name == "Neu"

    deleted_ok = service.delete_item(created.id)
    assert deleted_ok is True
    assert service.get_item(created.id) is None

    # delete auf nicht existierend → False
    assert service.delete_item(999_999) is False
