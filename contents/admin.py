from django.contrib import admin
from .models import Category, Post, ArchievedPost


class PPostInline(admin.TabularInline):
    model = Post
    fields = ("title", "status")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(status=Post.Statuses.PUBLISHED)


class DPostInline(admin.TabularInline):
    model = Post
    fields = ("title", "status")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(status=Post.Statuses.DRAFT)


class UPPostInline(admin.TabularInline):
    model = Post
    fields = ("title", "status")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(status=Post.Statuses.UNPUBLISHED)

# --------------------------------------------------------------------------------

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [PPostInline, DPostInline, UPPostInline]
    list_display = ("name", "parent")
    search_fields = ("name",)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.prefetch_related("cat_posts")
        return queryset


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "publisher", "category", "status")
    list_filter = ("is_active", "status")
    readonly_fields = ("created_at", "updated_at")
    search_fields = ("title", "body")

    actions = (
        "change_status_to_published",
        "change_status_to_draft",
        "change_status_to_unpublished",
    )

    @admin.action(description="change status to published")
    def change_status_to_published(self, request, queryset):
        queryset.update(status=Post.Statuses.PUBLISHED)

    @admin.action(description="change status to draft")
    def change_status_to_draft(self, request, queryset):
        queryset.update(status=Post.Statuses.DRAFT)

    @admin.action(description="change status to unpublished")
    def change_status_to_unpublished(self, request, queryset):
        queryset.update(status=Post.Statuses.UNPUBLISHED)


@admin.register(ArchievedPost)
class ArchievedPostAdmin(admin.ModelAdmin):
    list_display = ("title", "publisher", "category", "status")
    readonly_fields = ("created_at", "updated_at")
    search_fields = ("title", "body")

    actions = ("activate_post",)

    def get_queryset(self, request):
        return ArchievedPost.objects.filter(is_active=False)

    @admin.action(description="Activate selected posts")
    def activate_form(self, request, queryset):
        queryset.update(is_active=True)
