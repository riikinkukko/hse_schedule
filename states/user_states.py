from aiogram.fsm.state import State, StatesGroup

class UserStates(StatesGroup):
    waiting_for_schedule = State()
    waiting_for_subject_search = State()
    main_menu = State()