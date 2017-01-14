from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Institution(models.Model):
    # Relationships
    parent = models.ForeignKey(
        'self',
        on_delete = models.PROTECT,
        blank = True,
        null = True,
    )
    
    # Attributes
    name = models.CharField(max_length = 64)
    short_name = models.CharField(max_length = 16)

    # Manager


    # Functions
    def __str__(self):
        if self.parent is None:
            ustr = '{}'.format(self.name) 
        else:
            ustr = '{}, {}'.format(self.name, self.parent)

        return ustr

    # Meta
    class Meta:
        order_with_respect_to = 'parent'

class Department(models.Model):
    institution = models.ForeignKey(
        Institution,
        on_delete = models.PROTECT
    )

    chair = models.ForeignKey(
        User,
        on_delete = models.PROTECT,
    )

    name = models.CharField(max_length=128)
    abbreviation = models.CharField(max_length=8)

    def __str__(self):
        return '{} ({})'.format(self.name, self.institution.short_name)

    class Meta:
        order_with_respect_to = 'institution'

class Program(models.Model):
    institution = models.ForeignKey(
        Institution,
        on_delete = models.PROTECT,
    )
    
    chair = models.ForeignKey(
        User,
        on_delete = models.PROTECT,
    )
    
    name = models.CharField(max_length=128)

    abbreviation = models.CharField(max_length=8)
    
    def __str__(self):
        return '{} ({})'.format(self.name, self.institution.short_name)

    class Meta:
        order_with_respect_to = 'institution'

class LeadershipTitle(models.Model):
    title = models.CharField(
        max_length = 128,
        unique = True,
    )
    title_abbrev = models.CharField(
        max_length = 16,
        blank = True,
        null = True,
    )
    notes = models.TextField(
        blank = True,
        null = True,
    )

    def __str__(self):
        return '{}'.format(self.title)

class Workgroup(models.Model): # Labs, etc.
    # What department is this group associated with?
    department = models.ForeignKey(
        Department,
        related_name = "workgroup",
        on_delete = models.PROTECT,
    )

    # What program is this group associated with?
    program = models.ManyToManyField(Program)

    # Who leads the group? E.g. principal investigator, manager, director 
    lead = models.ForeignKey(
        User,
        related_name = "workgroup",
        on_delete = models.PROTECT,
    )

    # What is the lead's title? Default = PI
    lead_title = models.ForeignKey(
        LeadershipTitle,
        related_name = "lead_title",
        on_delete = models.PROTECT,
    )
    
    # What is this group called?
    name = models.CharField(max_length = 128)

    # Where is this group located? E.g. building and room
    location = models.CharField(
        max_length = 128,
    )

    # Build the display string for this group from the group name and the instution(s) it is affiliated with. Every group is required to be associated with a department, but zero or multiple programs.
    def __str__(self):
        # Start with the group name and the department institution
        workgroup_str = '{}, {}'.format(self.name, self.department.institution.short_name)
        
        # Now add the program institution(s) if the group is associated with one, but only unique ones via distinct() call. No need to repeat. Add the short_name to the string.
        if self.program:
            for inst in self.program.all().values('institution').distinct():
                 workgroup_str += '/%s' % (Institution.objects.get(pk=inst['institution']).short_name)

        return workgroup_str

    class Meta:
        ordering = ['name']

class FundingType(models.Model):
    """
    List from "Types of Awards" described by Johns Hopkins Office of \
    Research Administration http://www.hopkinsmedicine.org/research/synergy/\
    ora/handbook/handbook_II.html
    """

    name = models.CharField(
        max_length = 64,
        unique = True,
    )
    short_name = models.CharField(
        max_length = 16,
        blank = True,
        null = True,
    )
    notes = models.TextField(
        blank = True,
        null = True,
    )
    
    def __str__(self):
        return '{}'.format(self.name)

class Funding(models.Model):
    # Define lists of choices; potentially split this off later
    # List from "Types of Awards" described by Johns Hopkins Office of Research Administration http://www.hopkinsmedicine.org/research/synergy/ora/handbook/handbook_II.html

    # Who was this awarded to?
    awarded_to = models.ForeignKey(
        User,
        on_delete = models.PROTECT,
    )

    # What type of funding is this? Default = grant
    funding_type = models.ForeignKey(
        FundingType,
        on_delete = models.PROTECT,
    )
    
    # Where did this funding come from? E.g. agency (NIH, NSF, HHS, USDA, DoD, individual, etc.)
    funding_source = models.CharField(
        max_length=64
    )
    
    # What is the name of this award?
    name = models.CharField(
        verbose_name = "Award name",
        max_length = 128,
    )

    short_name = models.CharField(
        max_length=32
    )

    # What is the award number? N/A for none
    number = models.CharField(
        verbose_name = "Award number",
        max_length = 64,
    )
    
    # What is the internal grant code for this award? Tufts uses a DeptID-GrantCode format.
    dept_id = models.CharField(
        verbose_name = 'Dept ID',
        max_length = 7
    )
    grant_code = models.CharField(
        max_length = 6,
        blank = True
    )

    # What are the active dates of this funding?
    start_date = models.DateField()
    end_date = models.DateField()

    # What is the abstract or description of this award?
    abstract = models.TextField(
        blank = True,
    )
    
    def __str__(self):
        return '{}-{} ({} {}, {})'.format(self.dept_id, self.grant_code, self.short_name, self.funding_type, self.awarded_to)

    def deptid_grantcode(self):
        return '{}-{}'.format(self.dept_id, self.grant_code)

    class Meta:
        verbose_name_plural = "Funding"
        ordering = ['-end_date']
