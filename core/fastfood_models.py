from django.db import models

class TblAcc(models.Model):
    ref = models.AutoField(primary_key=True, db_column='Ref')
    stud_id = models.CharField(max_length=15, db_column='StudID')
    balance = models.IntegerField(db_column='Balance')
    date_entered = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_acc'


class TblFood(models.Model):
    id = models.AutoField(primary_key=True, db_column='ID')
    food_code = models.CharField(max_length=100)
    food_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    img = models.TextField(blank=True, null=True)
    food_seq = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tbl_food'


class TblPos(models.Model):
    id = models.AutoField(primary_key=True, db_column='ID')
    trans_no = models.CharField(max_length=100)
    trans_date = models.DateField()
    trans_month = models.CharField(max_length=100)
    food_code = models.CharField(max_length=100)
    food_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    qty = models.CharField(max_length=100)
    totalprice = models.DecimalField(max_digits=10, decimal_places=2)
    grandtotal = models.DecimalField(max_digits=10, decimal_places=2)
    nooffoods = models.CharField(max_length=100)
    customerid = models.CharField(max_length=90, db_column='customerID')
    

    class Meta:
        managed = False
        db_table = 'tbl_pos'


class TblStudentInfo(models.Model):
    ref = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=90, db_column='FirstName')
    last_name = models.CharField(max_length=90, db_column='LastName')
    middle_name = models.CharField(max_length=90, blank=True, null=True, db_column='MiddleName')
    stud_id = models.CharField(max_length=15, db_column='StudID')
    img = models.TextField()
    sex = models.CharField(max_length=90)

    class Meta:
        managed = False
        db_table = 'tbl_studentinfo'


class TblSysAcc(models.Model):
    ref = models.AutoField(primary_key=True, db_column='Ref')
    username = models.CharField(max_length=90)
    password = models.CharField(max_length=90)
    category = models.CharField(max_length=90)

    class Meta:
        managed = False
        db_table = 'tbl_sysacc'
