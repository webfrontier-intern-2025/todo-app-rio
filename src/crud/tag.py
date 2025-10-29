from src.models.tag import Tag


def get_tags(db):
    return db.query(Tag).all()


def create_tag(db, name: str):
    tag = Tag(name=name)
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag


def delete_tag(db, tag_id: int):
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if tag:
        db.delete(tag)
        db.commit()


def get_all_tags(db):
    """全てのタグを取得"""
    return db.query(Tag).order_by(Tag.id).all()
