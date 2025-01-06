from django.db import models
from django.forms import CharField
from django.utils import timezone

# Create your models here.
class User(models.Model):
    full_name = models.CharField(max_length=100000000)
    email = models.CharField(max_length=100000000)
    password = models.CharField(max_length=100000000)
    salt = models.CharField(max_length=1023)
    FRESHMAN = "FR"
    SOPHOMORE = "SO"
    JUNIOR = "JR"
    SENIOR = "SR"
    YEAR_IN_SCHOOL_CHOICES = {
        FRESHMAN: "Freshman",
        SOPHOMORE: "Sophomore",
        JUNIOR: "Junior",
        SENIOR: "Senior",
    }
    grade_level = models.CharField(
        max_length=5000,
        choices=YEAR_IN_SCHOOL_CHOICES,
        default=FRESHMAN,
    )
    schedules = models.TextField(max_length=100000000)
    course_catalog = models.FileField(upload_to='media')
    high_school_gpa_w = models.FloatField()
    high_school_gpa_uw = models.FloatField()
    sat_reading = models.IntegerField()
    sat_math = models.IntegerField()
    act = models.IntegerField()
    chosen_major = models.CharField(max_length=100000000)
    LOW_TIER = "LT"
    MID_TIER = "MT"
    TOP_TIER = "TT"
    COLLEGE_LEVEL = {
        LOW_TIER: "Low Tier",
        MID_TIER: "Mid Tier",
        TOP_TIER: "Top Tier"
    }
    college_level = models.CharField(
        max_length=5000,
        choices=COLLEGE_LEVEL,
        default=MID_TIER,
    )
    extracurr_awards = models.TextField(max_length=100000000)
    notes = models.TextField(max_length=100000000)
    score = models.FloatField()

    def __str__(self):
        return '%s - %s' % (self.full_name, self.grade_level)


class NormalChatHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    history = models.TextField(max_length=1000000000000000000) 

class SchedChatHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    history = models.TextField(max_length=1000000000000000000)

class TutorChatHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    history = models.TextField(max_length=1000000000000000000)

class College(models.Model):
    name = models.CharField(max_length=100000000)
    acceptance_rate = models.FloatField()
    location = models.CharField(max_length=100000000)
    tuition_out_of_state = models.FloatField()
    high_school_gpa_w = models.FloatField()
    high_school_gpa_uw = models.FloatField()
    sat_reading = models.IntegerField()
    sat_math = models.IntegerField()
    act = models.IntegerField()
    extracurr_awards = models.IntegerField()
    score = models.FloatField()
    def __str__(self):
        return '%s - %s' % (self.name, self.acceptance_rate)


class CollegeList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    essays = models.BooleanField() 
    score_report = models.BooleanField() 
    sat_report = models.BooleanField() 
    additional_questions = models.BooleanField() 

    def __str__(self):
        return '%s - %s' % (self.user, self.college)
    