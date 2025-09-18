def position_size(deposit: float, risk_percent: float, stop_loss: float) -> float:
    """
    Рассчёт размера позиции.
    deposit       - депозит в USDT
    risk_percent  - риск в %
    stop_loss     - размер стопа в $
    """
    risk_amount = deposit * (risk_percent / 100)
    size = risk_amount / stop_loss
    return size
