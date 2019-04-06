from django.contrib import admin

from .models import HardwareItem, HardwareAdmin, InfoSection, HackerProfile, ShirtSize, ShirtSizeAdmin, \
    DietaryRestriction, DietaryRestrictionAdmin, Team, TeamAdmin, HackerAdmin, BreakfastChoice, BreakfastChoiceAdmin, LunchChoice, LunchChoiceAdmin, \
    DinnerChoice, DinnerChoiceAdmin

admin.site.register(InfoSection)
admin.site.register(HackerProfile, HackerAdmin)
admin.site.register(ShirtSize, ShirtSizeAdmin)
admin.site.register(DietaryRestriction, DietaryRestrictionAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(HardwareItem, HardwareAdmin)
admin.site.register(BreakfastChoice, BreakfastChoiceAdmin)
admin.site.register(LunchChoice, LunchChoiceAdmin)
admin.site.register(DinnerChoice, DinnerChoiceAdmin)
