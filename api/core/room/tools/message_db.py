from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from core.room.models.message import Message
from sqlalchemy.exc import SQLAlchemyError

async def add_message(
    session: AsyncSession,
    sender_id: int, 
    room_id: int, 
    content: str,
) -> Message:
    """
    Добавляем новое сообщение в базу данных.
    :param session: Асинхронная сессия базы данных.
    :param sender_id: Идентификатор отправителя
    :param room_id: ID комнаты, к которой привязано сообщение.
    :param content: Содержимое сообщения
    :return: Созданное сообщение
    """
    try:
        new_message = Message(
            room_id=room_id,
            sender_id = sender_id,
            content = content
        )
        session.add(new_message)
        await session.commit()
        await session.refresh(new_message)
        return new_message
    except SQLAlchemyError as e:
        # Откат транзакции в случае ошибки
        await session.rollback()
        raise Exception(f"Ошибка при сохранении метаданных файла: {str(e)}")
