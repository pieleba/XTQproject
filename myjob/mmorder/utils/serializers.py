
from rest_framework import serializers


#自定义营养小知识序列化类
from mmorder.models import Knowledge


class KnowledgeSerializers(serializers.ModelSerializer):

    class Meta:
        model=Knowledge # 关联小知识模型
        fields="__all__" # 序列化小知识所有类属性