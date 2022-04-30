from flask_pagedown.fields import PageDownField
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, Regexp, ValidationError

from app.models import Role, User


class EditProfileForm(FlaskForm):
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')


class EditProfileAdminForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1,64), Email()])
    username = StringField('Username（只能使用大小写字母、数字、点和下划线）', validators=[DataRequired(), Length(1,64),
                                                   Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                          'Usernames must have only letters, numbers, dots or underscores')])
    confirmed = BooleanField('Confirmed')
    role = SelectField('Role', coerce=int)
    # 元组中的标识符是角色的id,coerce=int 参数，把字段的值转换为整数，而不使用默认的字符串。

    name = StringField('Real name', validators=[Length(0,64)])
    location = StringField('Location', validators=[Length(0,64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        """SelectField 实例必须在其choices 属性中设置各选项。选项必须是一个由元组构成的列表，
        各元组都包含两个元素：选项的标识符，以及显示在控件中的文本字符串。choices 列表在表单的构造函数中设定"""
        self.role.choices = [(role.id, role.name) for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if field.data !=self.user.username and User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')


class PostForm(FlaskForm):
    body = PageDownField("您想发点什么？（下面使用MarkDown文本编辑器并支持实时预览）", validators=[DataRequired()])
    submit = SubmitField("提交")


class CommentForm(FlaskForm):
    body = StringField('发表您的评论：', validators=[DataRequired()])
    submit = SubmitField('提交')