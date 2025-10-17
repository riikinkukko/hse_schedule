from aiogram.fsm.state import State, StatesGroup

class UserStates(StatesGroup):
    waiting_for_schedule = State()
    main_menu = State()