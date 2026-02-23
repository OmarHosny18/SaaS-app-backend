from rest_framework import serializers


class StatusCountSerializer(serializers.Serializer):
    status = serializers.CharField()
    count = serializers.IntegerField()


class MonthlyApplicationSerializer(serializers.Serializer):
    month = serializers.DateField()
    count = serializers.IntegerField()


class TopTitleSerializer(serializers.Serializer):
    job_title = serializers.CharField()
    count = serializers.IntegerField()


class TopLocationSerializer(serializers.Serializer):
    location = serializers.CharField()
    count = serializers.IntegerField()


class DashboardSerializer(serializers.Serializer):
    total_applications = serializers.IntegerField()
    applications_this_month = serializers.IntegerField()
    interview_rate = serializers.DecimalField(max_digits=5, decimal_places=2)
    offer_rate = serializers.DecimalField(max_digits=5, decimal_places=2)
    rejection_rate = serializers.DecimalField(max_digits=5, decimal_places=2)
    by_status = StatusCountSerializer(many=True)
    over_time = MonthlyApplicationSerializer(many=True)
    top_titles = TopTitleSerializer(many=True)
    top_locations = TopLocationSerializer(many=True)