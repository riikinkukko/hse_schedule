from aiogram.fsm.state import State, StatesGroup

class UserStates(StatesGroup):
    waiting_for_schedule = State()
    waiting_for_subject_search = State()
    main_menu = State()
    waiting_for_cst_group = State()
    waiting_for_eng_group = State()
    waiting_for_new_cst_group = State()
    waiting_for_new_eng_group = State()