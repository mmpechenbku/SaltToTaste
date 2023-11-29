from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from .models import Recipe, Ingredient, CommentRecipe, RecipeStep, SaveRecipe, IngredientQuantity, Selection, LikeComment

class IngredientQuantityInline(admin.TabularInline):
    model = IngredientQuantity
    extra = 0
    # raw_id_fields = ['ingredient']

class RecipeStepInline(admin.StackedInline):
    model = RecipeStep
    extra = 1

class RecipeAdmin(admin.ModelAdmin):
    inlines = [IngredientQuantityInline, RecipeStepInline]

    class Media:
        js = ('js/admin.js',)

admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient)
admin.site.register(RecipeStep)
admin.site.register(SaveRecipe)
admin.site.register(IngredientQuantity)
admin.site.register(Selection)




@admin.register(CommentRecipe)
class CommentAdminPage(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title', 'recipe', 'author', 'time_create', 'status')
    mptt_level_indent = 2
    list_display_links = ('recipe',)
    list_filter = ('time_create', 'time_update', 'author')
    list_editable = ('status',)

admin.site.register(LikeComment)

# Register your models here.
