from django.contrib.auth.models import User
from rest_framework import serializers
from money_manager.models import Category, Transaction, Balance


class TransactionSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    category_name_id = serializers.SerializerMethodField('category_name')

    @ staticmethod
    def category_name(self):
        return Category.objects.filter(pk=self.category.id)[0].category_name

    class Meta:
        model = Transaction
        fields = (
            'id', 'user', 'category_name_id', 'category', 'date_of_transaction',
            'time_of_transaction', 'amount_of_transaction', 'organisation', 'comment'
        )

    def create(self, validated_data):
        obj_for_change = Category.objects.filter(user=self.context['request'].user,
                                                 category_name=validated_data['category']).first()
        changes = validated_data['amount_of_transaction']
        obj_for_change.total += changes
        obj_for_change.save()
        bal_for_change = Balance.objects.filter(user=self.context['request'].user).first()
        bal_for_change.balance += changes
        bal_for_change.save()
        return Transaction.objects.create(user=self.context['request'].user, **validated_data)

    def update(self, instance, validated_data):
        cat_for_change = Category.objects.filter(user=instance.user, category_name=instance.category).first()
        minus_changes = instance.amount_of_transaction
        cat_for_change.total -= minus_changes
        cat_for_change.save()
        bal_for_change = Balance.objects.filter(user=instance.user).first()
        bal_for_change.balance -= minus_changes
        bal_for_change.save()
        obj_for_change = Category.objects.filter(user=self.context['request'].user,
                                                 category_name=validated_data['category']).first()
        plus_changes = validated_data['amount_of_transaction']
        obj_for_change.total += plus_changes
        obj_for_change.save()
        bal_for_change = Balance.objects.filter(user=self.context['request'].user).first()
        bal_for_change.balance += plus_changes
        bal_for_change.save()

        instance.amount_of_transaction = validated_data.get('amount_of_transaction', instance.amount_of_transaction)
        instance.date_of_transaction = validated_data.get('date_of_transaction', instance.date_of_transaction)
        instance.time_of_transaction = validated_data.get('time_of_transaction', instance.time_of_transaction)
        instance.category = validated_data.get('category', instance.category)
        instance.organisation = validated_data.get('organisation', instance.organisation)
        instance.comment = validated_data.get('comment', instance.comment)
        instance.save()
        return instance


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'category_name', 'total')
        read_only_fields = ('id', 'total')

    def create(self, validated_data):
        list_of_categories = Category.objects.filter(user=self.context['request'].user) \
            .values_list('category_name', flat=True)
        if validated_data['category_name'] in list_of_categories:
            raise serializers.ValidationError('The category {0} had '
                                              'been already created'.format(validated_data['category_name']))
        else:
            return Category.objects.create(user=self.context['request'].user,
                                           category_name=validated_data['category_name'])


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Balance
        fields = ('balance',)


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    extra_kwargs = {'password': {'write_only': True},
                    'password2': {'write_only': True}}

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')

    def create(self, validated_data):
        if validated_data['password'] != validated_data['password2']:
            raise serializers.ValidationError('The passwords are not the similar')
        return User.objects.create_user(username=validated_data['username'],
                                        email=validated_data['email'],
                                        password=validated_data['password'])
