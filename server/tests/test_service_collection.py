import pytest
from unittest.mock import MagicMock, patch
from app.services.collection_service import (
    create_collection_v1,
    get_collection_by_id_v1,
    update_collection_v1,
    delete_collection_v1,
    get_all_collections_v1
)
from app.schemas.collection import CollectionCreate, CollectionUpdate
from app.models.collection import Collection
from app.core.errors import AppException
from app.api.dependencies import PaginationParams, SearchParams

def test_get_all_collections_v1():
    db = MagicMock()
    pagination = PaginationParams(page=1, size=10)
    search = SearchParams(q="Vintage")
    
    with patch("app.services.collection_service.paginate_query") as mock_paginate:
        mock_paginate.return_value = {"items": [], "total": 0}
        get_all_collections_v1(db, pagination, search)
        assert db.query.called
        assert mock_paginate.called

def test_create_collection_success():
    db = MagicMock()
    coll_in = CollectionCreate(title="My Collection", description="A cool collection")
    
    result = create_collection_v1(db, coll_in, current_user_id=1)
    
    assert result.title == "My Collection"
    assert result.owner_id == 1
    assert db.add.called

def test_update_collection_permission_denied():
    db = MagicMock()
    mock_coll = Collection(id=1, title="Old Title", owner_id=10)
    db.query().filter().first.return_value = mock_coll
    
    coll_in = CollectionUpdate(title="New Title")
    # Người dùng 20 cố sửa bộ sưu tập của người 10
    with pytest.raises(AppException) as exc:
        update_collection_v1(db, 1, coll_in, current_user_id=20)
    assert exc.value.status_code == 403

def test_delete_collection_success():
    db = MagicMock()
    mock_coll = Collection(id=1, owner_id=10)
    db.query().filter().first.return_value = mock_coll
    
    delete_collection_v1(db, 1, current_user_id=10)
    assert db.delete.called
    assert db.commit.called
