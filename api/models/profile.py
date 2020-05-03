from . import db


class Profile(db.Model):
    __tablename__ = "profiles"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('public.user.user_id'), nullable=False)
    home_course = db.Column(db.String)
    dexterity = db.Column(db.String)

    def __init__(self, **kwargs):
        self.user_id = kwargs.get('user_id')
        self.home_course = kwargs.get('home_course')
        self.dexterity = kwargs.get('dexterity')

    def save(self):
        """
        Persist the User's Profile in the database
        :param:
        :return: Id of Profile record
        """
        db.session.add(self)
        db.session.commit()
        return self.id

    def update(self):
        """
        Update an existing user profile in the database
        :param:
        :return: Id of Profile record
        """
        db.session.merge(self)
        db.session.commit()
        return self.id

    @staticmethod
    def get_by_id(user_id):
        """
        Query a User's Profile by their user id
        :param: email
        :return: User or None
        """
        return Profile.query.filter_by(user_id=user_id).first()
