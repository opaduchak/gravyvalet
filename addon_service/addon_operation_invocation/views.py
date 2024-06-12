from addon_service.common.permissions import (
    IsAuthenticated,
    SessionUserIsOwner,
    SessionUserMayAccessInvocation,
    SessionUserMayPerformInvocation,
)
from addon_service.common.viewsets import RetrieveWriteViewSet
from addon_toolkit import AddonOperationType

from .models import AddonOperationInvocation
from .perform import perform_invocation__blocking
from .serializers import AddonOperationInvocationSerializer


class AddonOperationInvocationViewSet(RetrieveWriteViewSet):
    queryset = AddonOperationInvocation.objects.all()
    serializer_class = AddonOperationInvocationSerializer

    def get_permissions(self):
        match self.action:
            case "retrieve" | "retrieve_related":
                return [IsAuthenticated(), SessionUserMayAccessInvocation()]
            case "partial_update" | "update" | "destroy":
                return [IsAuthenticated(), SessionUserIsOwner()]
            case "create":
                return [IsAuthenticated(), SessionUserMayPerformInvocation()]
            case None:
                return super().get_permissions()
            case _:
                raise NotImplementedError(
                    f"no permission implemented for action '{self.action}'"
                )

    def perform_create(self, serializer):
        super().perform_create(serializer)
        # after creating the AddonOperationInvocation, look into invoking it
        _invocation = serializer.instance
        _operation_type = _invocation.operation.operation_type
        match _operation_type:
            case AddonOperationType.REDIRECT | AddonOperationType.IMMEDIATE:
                perform_invocation__blocking(_invocation)
            case AddonOperationType.EVENTUAL:
                raise NotImplementedError("TODO: enqueue task")
            case _:
                raise ValueError(f"unknown operation type: {_operation_type}")
