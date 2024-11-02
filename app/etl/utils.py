# utils.py
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

async def transaction_handler(db: AsyncSession, func, *args, **kwargs):
    """
    Handle a database transaction with automatic commit and rollback.
    
    Args:
        db (AsyncSession): Database session.
        func (Callable): Function to execute within the transaction.
        *args: Positional arguments to pass to func.
        **kwargs: Keyword arguments to pass to func.
    
    Returns:
        Any: The result of the function execution.
    """
    try:
        result = await func(*args, **kwargs)
        await db.commit()
        return result
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Operation failed: {e}"
        )
