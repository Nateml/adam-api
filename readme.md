A python interface to access marks from ADAM. Limited functionality.
Only works with Oakhill adam at this stage.

USAGE:

- create a new session object with Session(username, password, type)
    type is a string which describes the type of login, namely 'pupil', 'staff', or 'parent'.
    all interactions with adam will happen through this object.

- retrieve marks by using <your_session_object>.get_marks(term_index)
    term_index is an int which refers to the index the desired term is found in the list returned by <your_session_object>.terms()
    access different terms as you would access a list (0 for the most recent term, -1 for last term)

    an optional <subject> parameter can be included like so: <your_session_object>.get_marks(term_index, subject=<string>)
    This will return a list of tuples containing your marks for each assessment you completed in a specific term for a specific subject