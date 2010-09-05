from django.contrib import admin

from main.models import Client, Show, Location, Raw_File, Quality, Episode, Cut_List, State, Log

class ClientAdmin(admin.ModelAdmin):
    list_display = ('sequence', 'name', 'description',)
    list_display_links = ('name',)
    admin_order_field = ('sequence', 'name',)
    prepopulated_fields = {"slug": ("name",)}
admin.site.register(Client, ClientAdmin)

class ShowAdmin(admin.ModelAdmin):
    list_display = ('sequence', 'client','name',)
    list_display_links = ('name',)
    admin_order_field = ('sequence', 'name',)
    prepopulated_fields = {"slug": ("name",)}
admin.site.register(Show, ShowAdmin)

class LocationAdmin(admin.ModelAdmin):
    list_display = ('id','sequence', 'default', 'name','slug')
    list_display_links = ('id',)
    list_editable = ('default', 'name','slug')
    admin_order_field = ('sequence', 'name',)
    prepopulated_fields = {"slug": ("name",)}
admin.site.register(Location, LocationAdmin)

class Raw_FileAdmin(admin.ModelAdmin):
    list_display = ('filename', 'show', 'location', 'start', 'duration', 'end', ) 
    list_display_links = ('filename',)
    list_filter = ('location',)
    search_fields = ['filename']
admin.site.register(Raw_File, Raw_FileAdmin)

class QualityAdmin(admin.ModelAdmin):
    list_display = ('level', 'name','description')
    admin_order_field = ('level',)
    # list_editable = list_display
admin.site.register(Quality, QualityAdmin)

class EpisodeAdmin(admin.ModelAdmin):

    def state_bumper(self,obj):
        return '<input type="submit" value="+" class=pb>' 
    state_bumper.allow_tags = True
    state_bumper.short_description = 'bump'

    list_display = (
        'location', 
	'sequence', 'name', 'state', 'state_bumper', 
        'locked','locked_by',
        'show', 
        'start','end','target')
    # list_display = ( 'sequence', 'name', 'state', 'state_bumper', 'duration' )
    ordering = ('sequence', )
    date_hierarchy = 'start'
    list_display_links = ('name',)
    list_editable = ('state','locked','locked_by', )
    # list_editable = ('state','duration')
    admin_order_field = ('sequence', 'name',)
    list_filter = ('state','location','locked','locked_by')
    search_fields = ['name']
    prepopulated_fields = {"slug": ("name",)}
    save_on_top=True
    class Media:
        js = ("/static/js/jquery.js","/static/js/bumpbut.js",)
admin.site.register(Episode, EpisodeAdmin)

class Cut_ListAdmin(admin.ModelAdmin):
    list_display = ('sequence', 'episode', 'raw_file',)
    admin_order_field = list_display
admin.site.register(Cut_List, Cut_ListAdmin)

class StateAdmin(admin.ModelAdmin):
    list_display = ('slug', 'description',)
    admin_order_field = ('slug', )
admin.site.register(State, StateAdmin)

class LogAdmin(admin.ModelAdmin):
    pass
admin.site.register(Log, LogAdmin)

