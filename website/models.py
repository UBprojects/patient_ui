from patient_ui.models import *


class Patient(models.Model):
    auth_user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    dob = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, default='F', null=True, blank=True)
    is_married = models.BooleanField(default=False)
    about = models.TextField(blank=True, null=True)
    profile_url = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'patient'


class DiseaseMaster(models.Model):
    title = models.CharField(max_length=150, db_index=True)

    class Meta:
        managed = True
        db_table = 'disease_master'


class SymptomMaster(models.Model):
    title = models.CharField(max_length=150, db_index=True)

    class Meta:
        managed = True
        db_table = 'symptom_master'


class RiskFactorMaster(models.Model):
    title = models.CharField(max_length=150, db_index=True)

    class Meta:
        managed = True
        db_table = 'risk_factor_master'


class DiseaseSymptomMapping(models.Model):
    disease = models.ForeignKey(DiseaseMaster, models.DO_NOTHING)
    symptom = models.ForeignKey(SymptomMaster, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'disease_symptom_mapping'


class DiseaseRiskFactorMapping(models.Model):
    disease = models.ForeignKey(DiseaseMaster, models.DO_NOTHING)
    risk_factor = models.ForeignKey(RiskFactorMaster, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'disease_risk_factor_mapping'


class DiseaseInfo(models.Model):
    patient = models.ForeignKey(Patient, models.DO_NOTHING)
    disease = models.ForeignKey(DiseaseMaster, models.DO_NOTHING)
    diagnosed_on = models.DateField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'disease_info'


class Post(models.Model):
    auth_user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    text = models.TextField()
    created_at = models.DateField()
    num_replies = models.IntegerField(default=0)

    class Meta:
        managed = True
        db_table = 'post'


class PostReply(models.Model):
    auth_user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    post = models.ForeignKey(Post, models.DO_NOTHING)
    text = models.TextField()

    class Meta:
        managed = True
        db_table = 'post_reply'


class Category(models.Model):
    title = models.CharField(max_length=100)

    class Meta:
        managed = True
        db_table = 'category'


class SubCategory(models.Model):
    category = models.ForeignKey(Category, models.DO_NOTHING)
    title = models.CharField(max_length=150)

    class Meta:
        managed = True
        db_table = 'sub_category'


class CategoryPriority(models.Model):
    auth_user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    category = models.ForeignKey(Category, models.DO_NOTHING)
    order = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'category_priority'
