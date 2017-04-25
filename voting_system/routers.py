class dbRouter(object):
    """
    A router to control all database operations on models in the
    auth application.
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read auth models go to auth_db.
        """
        if model._meta.app_label == 'admin':
            return 'default'
        elif model._meta.app_label == 'auth':
            return 'voter_auth'
        elif model._meta.app_label == 'reg1':
            return 'region1'
        elif model._meta.app_label == 'reg2':
            return 'region2'
        elif model._meta.app_label == 'people':
            return 'people'
        elif model._meta.app_label == 'gov_verify':
            return 'gov_verify'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth models go to auth_db.
        """
        if model._meta.app_label == 'admin':
            return 'default'
        elif model._meta.app_label == 'auth':
            return 'voter_auth'
        elif model._meta.app_label == 'reg1':
            return 'region1'
        elif model._meta.app_label == 'reg2':
            return 'region2'
        elif model._meta.app_label == 'people':
            return 'people'
        elif model._meta.app_label == 'gov_verify':
            return 'gov_verify'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth app is involved.
        """
        if obj1._meta.app_label == 'admin' or \
           obj2._meta.app_label == 'admin':
           return True
        if obj1._meta.app_label == 'auth' or \
           obj2._meta.app_label == 'auth':
           return True
        if obj1._meta.app_label == 'reg1' or \
           obj2._meta.app_label == 'reg1':
           return True
        if obj1._meta.app_label == 'reg2' or \
           obj2._meta.app_label == 'reg2':
           return True
        if obj1._meta.app_label == 'people' or \
           obj2._meta.app_label == 'people':
           return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the auth app only appears in the 'voterauth'
        database.
        """
        if app_label == 'admin':
            return db == 'default'
        if app_label == 'auth':
            return db == 'voterauth'
        if app_label == 'reg1':
            return db == 'region1'
        if app_label == 'reg2':
            return db == 'region2'
        if app_label == 'people':
            return db == 'people'
        return None