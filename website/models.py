from patient_ui.models import *


class Patient(models.Model):
    auth_user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    dob = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, default='F')
    is_married = models.BooleanField(default=False)
    about = models.TextField(blank=True, null=True)

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
