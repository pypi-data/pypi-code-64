# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from . import mobilecoind_api_pb2 as mobilecoind__api__pb2


class MobilecoindAPIStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.AddMonitor = channel.unary_unary(
        '/mobilecoind_api.MobilecoindAPI/AddMonitor',
        request_serializer=mobilecoind__api__pb2.AddMonitorRequest.SerializeToString,
        response_deserializer=mobilecoind__api__pb2.AddMonitorResponse.FromString,
        )
    self.RemoveMonitor = channel.unary_unary(
        '/mobilecoind_api.MobilecoindAPI/RemoveMonitor',
        request_serializer=mobilecoind__api__pb2.RemoveMonitorRequest.SerializeToString,
        response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
        )
    self.GetMonitorList = channel.unary_unary(
        '/mobilecoind_api.MobilecoindAPI/GetMonitorList',
        request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
        response_deserializer=mobilecoind__api__pb2.GetMonitorListResponse.FromString,
        )
    self.GetMonitorStatus = channel.unary_unary(
        '/mobilecoind_api.MobilecoindAPI/GetMonitorStatus',
        request_serializer=mobilecoind__api__pb2.GetMonitorStatusRequest.SerializeToString,
        response_deserializer=mobilecoind__api__pb2.GetMonitorStatusResponse.FromString,
        )
    self.GetUnspentTxOutList = channel.unary_unary(
        '/mobilecoind_api.MobilecoindAPI/GetUnspentTxOutList',
        request_serializer=mobilecoind__api__pb2.GetUnspentTxOutListRequest.SerializeToString,
        response_deserializer=mobilecoind__api__pb2.GetUnspentTxOutListResponse.FromString,
        )
    self.GenerateEntropy = channel.unary_unary(
        '/mobilecoind_api.MobilecoindAPI/GenerateEntropy',
        request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
        response_deserializer=mobilecoind__api__pb2.GenerateEntropyResponse.FromString,
        )
    self.GetAccountKey = channel.unary_unary(
        '/mobilecoind_api.MobilecoindAPI/GetAccountKey',
        request_serializer=mobilecoind__api__pb2.GetAccountKeyRequest.SerializeToString,
        response_deserializer=mobilecoind__api__pb2.GetAccountKeyResponse.FromString,
        )
    self.GetPublicAddress = channel.unary_unary(
        '/mobilecoind_api.MobilecoindAPI/GetPublicAddress',
        request_serializer=mobilecoind__api__pb2.GetPublicAddressRequest.SerializeToString,
        response_deserializer=mobilecoind__api__pb2.GetPublicAddressResponse.FromString,
        )
    self.ReadRequestCode = channel.unary_unary(
        '/mobilecoind_api.MobilecoindAPI/ReadRequestCode',
        request_serializer=mobilecoind__api__pb2.ReadRequestCodeRequest.SerializeToString,
        response_deserializer=mobilecoind__api__pb2.ReadRequestCodeResponse.FromString,
        )
    self.GetRequestCode = channel.unary_unary(
        '/mobilecoind_api.MobilecoindAPI/GetRequestCode',
        request_serializer=mobilecoind__api__pb2.GetRequestCodeRequest.SerializeToString,
        response_deserializer=mobilecoind__api__pb2.GetRequestCodeResponse.FromString,
        )
    self.ReadTransferCode = channel.unary_unary(
        '/mobilecoind_api.MobilecoindAPI/ReadTransferCode',
        request_serializer=mobilecoind__api__pb2.ReadTransferCodeRequest.SerializeToString,
        response_deserializer=mobilecoind__api__pb2.ReadTransferCodeResponse.FromString,
        )
    self.GetTransferCode = channel.unary_unary(
        '/mobilecoind_api.MobilecoindAPI/GetTransferCode',
        request_serializer=mobilecoind__api__pb2.GetTransferCodeRequest.SerializeToString,
        response_deserializer=mobilecoind__api__pb2.GetTransferCodeResponse.FromString,
        )
    self.ReadAddressCode = channel.unary_unary(
        '/mobilecoind_api.MobilecoindAPI/ReadAddressCode',
        request_serializer=mobilecoind__api__pb2.ReadAddressCodeRequest.SerializeToString,
        response_deserializer=mobilecoind__api__pb2.ReadAddressCodeResponse.FromString,
        )
    self.GetAddressCode = channel.unary_unary(
        '/mobilecoind_api.MobilecoindAPI/GetAddressCode',
        request_serializer=mobilecoind__api__pb2.GetAddressCodeRequest.SerializeToString,
        response_deserializer=mobilecoind__api__pb2.GetAddressCodeResponse.FromString,
        )
    self.GenerateTx = channel.unary_unary(
        '/mobilecoind_api.MobilecoindAPI/GenerateTx',
        request_serializer=mobilecoind__api__pb2.GenerateTxRequest.SerializeToString,
        response_deserializer=mobilecoind__api__pb2.GenerateTxResponse.FromString,
        )
    self.GenerateOptimizationTx = channel.unary_unary(
        '/mobilecoind_api.MobilecoindAPI/GenerateOptimizationTx',
        request_serializer=mobilecoind__api__pb2.GenerateOptimizationTxRequest.SerializeToString,
        response_deserializer=mobilecoind__api__pb2.GenerateOptimizationTxResponse.FromString,
        )
    self.GenerateTransferCodeTx = channel.unary_unary(
        '/mobilecoind_api.MobilecoindAPI/GenerateTransferCodeTx',
        request_serializer=mobilecoind__api__pb2.GenerateTransferCodeTxRequest.SerializeToString,
        response_deserializer=mobilecoind__api__pb2.GenerateTransferCodeTxResponse.FromString,
        )
    self.GenerateTxFromTxOutList = channel.unary_unary(
        '/mobilecoind_api.MobilecoindAPI/GenerateTxFromTxOutList',
        request_serializer=mobilecoind__api__pb2.GenerateTxFromTxOutListRequest.SerializeToString,
        response_deserializer=mobilecoind__api__pb2.GenerateTxFromTxOutListResponse.FromString,
        )
    self.SubmitTx = channel.unary_unary(
        '/mobilecoind_api.MobilecoindAPI/SubmitTx',
        request_serializer=mobilecoind__api__pb2.SubmitTxRequest.SerializeToString,
        response_deserializer=mobilecoind__api__pb2.SubmitTxResponse.FromString,
        )
    self.GetLedgerInfo = channel.unary_unary(
        '/mobilecoind_api.MobilecoindAPI/GetLedgerInfo',
        request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
        response_deserializer=mobilecoind__api__pb2.GetLedgerInfoResponse.FromString,
        )
    self.GetBlockInfo = channel.unary_unary(
        '/mobilecoind_api.MobilecoindAPI/GetBlockInfo',
        request_serializer=mobilecoind__api__pb2.GetBlockInfoRequest.SerializeToString,
        response_deserializer=mobilecoind__api__pb2.GetBlockInfoResponse.FromString,
        )
    self.GetBlock = channel.unary_unary(
        '/mobilecoind_api.MobilecoindAPI/GetBlock',
        request_serializer=mobilecoind__api__pb2.GetBlockRequest.SerializeToString,
        response_deserializer=mobilecoind__api__pb2.GetBlockResponse.FromString,
        )
    self.GetTxStatusAsSender = channel.unary_unary(
        '/mobilecoind_api.MobilecoindAPI/GetTxStatusAsSender',
        request_serializer=mobilecoind__api__pb2.GetTxStatusAsSenderRequest.SerializeToString,
        response_deserializer=mobilecoind__api__pb2.GetTxStatusAsSenderResponse.FromString,
        )
    self.GetTxStatusAsReceiver = channel.unary_unary(
        '/mobilecoind_api.MobilecoindAPI/GetTxStatusAsReceiver',
        request_serializer=mobilecoind__api__pb2.GetTxStatusAsReceiverRequest.SerializeToString,
        response_deserializer=mobilecoind__api__pb2.GetTxStatusAsReceiverResponse.FromString,
        )
    self.GetProcessedBlock = channel.unary_unary(
        '/mobilecoind_api.MobilecoindAPI/GetProcessedBlock',
        request_serializer=mobilecoind__api__pb2.GetProcessedBlockRequest.SerializeToString,
        response_deserializer=mobilecoind__api__pb2.GetProcessedBlockResponse.FromString,
        )
    self.GetBalance = channel.unary_unary(
        '/mobilecoind_api.MobilecoindAPI/GetBalance',
        request_serializer=mobilecoind__api__pb2.GetBalanceRequest.SerializeToString,
        response_deserializer=mobilecoind__api__pb2.GetBalanceResponse.FromString,
        )
    self.SendPayment = channel.unary_unary(
        '/mobilecoind_api.MobilecoindAPI/SendPayment',
        request_serializer=mobilecoind__api__pb2.SendPaymentRequest.SerializeToString,
        response_deserializer=mobilecoind__api__pb2.SendPaymentResponse.FromString,
        )
    self.PayAddressCode = channel.unary_unary(
        '/mobilecoind_api.MobilecoindAPI/PayAddressCode',
        request_serializer=mobilecoind__api__pb2.PayAddressCodeRequest.SerializeToString,
        response_deserializer=mobilecoind__api__pb2.SendPaymentResponse.FromString,
        )
    self.GetNetworkStatus = channel.unary_unary(
        '/mobilecoind_api.MobilecoindAPI/GetNetworkStatus',
        request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
        response_deserializer=mobilecoind__api__pb2.GetNetworkStatusResponse.FromString,
        )


class MobilecoindAPIServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def AddMonitor(self, request, context):
    """Monitors
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def RemoveMonitor(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetMonitorList(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetMonitorStatus(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetUnspentTxOutList(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GenerateEntropy(self, request, context):
    """Utilities
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetAccountKey(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetPublicAddress(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def ReadRequestCode(self, request, context):
    """b58 Codes
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetRequestCode(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def ReadTransferCode(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetTransferCode(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def ReadAddressCode(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetAddressCode(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GenerateTx(self, request, context):
    """Txs
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GenerateOptimizationTx(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GenerateTransferCodeTx(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GenerateTxFromTxOutList(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def SubmitTx(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetLedgerInfo(self, request, context):
    """Databases
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetBlockInfo(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetBlock(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetTxStatusAsSender(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetTxStatusAsReceiver(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetProcessedBlock(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetBalance(self, request, context):
    """Convenience calls
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def SendPayment(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def PayAddressCode(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetNetworkStatus(self, request, context):
    """Network status
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_MobilecoindAPIServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'AddMonitor': grpc.unary_unary_rpc_method_handler(
          servicer.AddMonitor,
          request_deserializer=mobilecoind__api__pb2.AddMonitorRequest.FromString,
          response_serializer=mobilecoind__api__pb2.AddMonitorResponse.SerializeToString,
      ),
      'RemoveMonitor': grpc.unary_unary_rpc_method_handler(
          servicer.RemoveMonitor,
          request_deserializer=mobilecoind__api__pb2.RemoveMonitorRequest.FromString,
          response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
      ),
      'GetMonitorList': grpc.unary_unary_rpc_method_handler(
          servicer.GetMonitorList,
          request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
          response_serializer=mobilecoind__api__pb2.GetMonitorListResponse.SerializeToString,
      ),
      'GetMonitorStatus': grpc.unary_unary_rpc_method_handler(
          servicer.GetMonitorStatus,
          request_deserializer=mobilecoind__api__pb2.GetMonitorStatusRequest.FromString,
          response_serializer=mobilecoind__api__pb2.GetMonitorStatusResponse.SerializeToString,
      ),
      'GetUnspentTxOutList': grpc.unary_unary_rpc_method_handler(
          servicer.GetUnspentTxOutList,
          request_deserializer=mobilecoind__api__pb2.GetUnspentTxOutListRequest.FromString,
          response_serializer=mobilecoind__api__pb2.GetUnspentTxOutListResponse.SerializeToString,
      ),
      'GenerateEntropy': grpc.unary_unary_rpc_method_handler(
          servicer.GenerateEntropy,
          request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
          response_serializer=mobilecoind__api__pb2.GenerateEntropyResponse.SerializeToString,
      ),
      'GetAccountKey': grpc.unary_unary_rpc_method_handler(
          servicer.GetAccountKey,
          request_deserializer=mobilecoind__api__pb2.GetAccountKeyRequest.FromString,
          response_serializer=mobilecoind__api__pb2.GetAccountKeyResponse.SerializeToString,
      ),
      'GetPublicAddress': grpc.unary_unary_rpc_method_handler(
          servicer.GetPublicAddress,
          request_deserializer=mobilecoind__api__pb2.GetPublicAddressRequest.FromString,
          response_serializer=mobilecoind__api__pb2.GetPublicAddressResponse.SerializeToString,
      ),
      'ReadRequestCode': grpc.unary_unary_rpc_method_handler(
          servicer.ReadRequestCode,
          request_deserializer=mobilecoind__api__pb2.ReadRequestCodeRequest.FromString,
          response_serializer=mobilecoind__api__pb2.ReadRequestCodeResponse.SerializeToString,
      ),
      'GetRequestCode': grpc.unary_unary_rpc_method_handler(
          servicer.GetRequestCode,
          request_deserializer=mobilecoind__api__pb2.GetRequestCodeRequest.FromString,
          response_serializer=mobilecoind__api__pb2.GetRequestCodeResponse.SerializeToString,
      ),
      'ReadTransferCode': grpc.unary_unary_rpc_method_handler(
          servicer.ReadTransferCode,
          request_deserializer=mobilecoind__api__pb2.ReadTransferCodeRequest.FromString,
          response_serializer=mobilecoind__api__pb2.ReadTransferCodeResponse.SerializeToString,
      ),
      'GetTransferCode': grpc.unary_unary_rpc_method_handler(
          servicer.GetTransferCode,
          request_deserializer=mobilecoind__api__pb2.GetTransferCodeRequest.FromString,
          response_serializer=mobilecoind__api__pb2.GetTransferCodeResponse.SerializeToString,
      ),
      'ReadAddressCode': grpc.unary_unary_rpc_method_handler(
          servicer.ReadAddressCode,
          request_deserializer=mobilecoind__api__pb2.ReadAddressCodeRequest.FromString,
          response_serializer=mobilecoind__api__pb2.ReadAddressCodeResponse.SerializeToString,
      ),
      'GetAddressCode': grpc.unary_unary_rpc_method_handler(
          servicer.GetAddressCode,
          request_deserializer=mobilecoind__api__pb2.GetAddressCodeRequest.FromString,
          response_serializer=mobilecoind__api__pb2.GetAddressCodeResponse.SerializeToString,
      ),
      'GenerateTx': grpc.unary_unary_rpc_method_handler(
          servicer.GenerateTx,
          request_deserializer=mobilecoind__api__pb2.GenerateTxRequest.FromString,
          response_serializer=mobilecoind__api__pb2.GenerateTxResponse.SerializeToString,
      ),
      'GenerateOptimizationTx': grpc.unary_unary_rpc_method_handler(
          servicer.GenerateOptimizationTx,
          request_deserializer=mobilecoind__api__pb2.GenerateOptimizationTxRequest.FromString,
          response_serializer=mobilecoind__api__pb2.GenerateOptimizationTxResponse.SerializeToString,
      ),
      'GenerateTransferCodeTx': grpc.unary_unary_rpc_method_handler(
          servicer.GenerateTransferCodeTx,
          request_deserializer=mobilecoind__api__pb2.GenerateTransferCodeTxRequest.FromString,
          response_serializer=mobilecoind__api__pb2.GenerateTransferCodeTxResponse.SerializeToString,
      ),
      'GenerateTxFromTxOutList': grpc.unary_unary_rpc_method_handler(
          servicer.GenerateTxFromTxOutList,
          request_deserializer=mobilecoind__api__pb2.GenerateTxFromTxOutListRequest.FromString,
          response_serializer=mobilecoind__api__pb2.GenerateTxFromTxOutListResponse.SerializeToString,
      ),
      'SubmitTx': grpc.unary_unary_rpc_method_handler(
          servicer.SubmitTx,
          request_deserializer=mobilecoind__api__pb2.SubmitTxRequest.FromString,
          response_serializer=mobilecoind__api__pb2.SubmitTxResponse.SerializeToString,
      ),
      'GetLedgerInfo': grpc.unary_unary_rpc_method_handler(
          servicer.GetLedgerInfo,
          request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
          response_serializer=mobilecoind__api__pb2.GetLedgerInfoResponse.SerializeToString,
      ),
      'GetBlockInfo': grpc.unary_unary_rpc_method_handler(
          servicer.GetBlockInfo,
          request_deserializer=mobilecoind__api__pb2.GetBlockInfoRequest.FromString,
          response_serializer=mobilecoind__api__pb2.GetBlockInfoResponse.SerializeToString,
      ),
      'GetBlock': grpc.unary_unary_rpc_method_handler(
          servicer.GetBlock,
          request_deserializer=mobilecoind__api__pb2.GetBlockRequest.FromString,
          response_serializer=mobilecoind__api__pb2.GetBlockResponse.SerializeToString,
      ),
      'GetTxStatusAsSender': grpc.unary_unary_rpc_method_handler(
          servicer.GetTxStatusAsSender,
          request_deserializer=mobilecoind__api__pb2.GetTxStatusAsSenderRequest.FromString,
          response_serializer=mobilecoind__api__pb2.GetTxStatusAsSenderResponse.SerializeToString,
      ),
      'GetTxStatusAsReceiver': grpc.unary_unary_rpc_method_handler(
          servicer.GetTxStatusAsReceiver,
          request_deserializer=mobilecoind__api__pb2.GetTxStatusAsReceiverRequest.FromString,
          response_serializer=mobilecoind__api__pb2.GetTxStatusAsReceiverResponse.SerializeToString,
      ),
      'GetProcessedBlock': grpc.unary_unary_rpc_method_handler(
          servicer.GetProcessedBlock,
          request_deserializer=mobilecoind__api__pb2.GetProcessedBlockRequest.FromString,
          response_serializer=mobilecoind__api__pb2.GetProcessedBlockResponse.SerializeToString,
      ),
      'GetBalance': grpc.unary_unary_rpc_method_handler(
          servicer.GetBalance,
          request_deserializer=mobilecoind__api__pb2.GetBalanceRequest.FromString,
          response_serializer=mobilecoind__api__pb2.GetBalanceResponse.SerializeToString,
      ),
      'SendPayment': grpc.unary_unary_rpc_method_handler(
          servicer.SendPayment,
          request_deserializer=mobilecoind__api__pb2.SendPaymentRequest.FromString,
          response_serializer=mobilecoind__api__pb2.SendPaymentResponse.SerializeToString,
      ),
      'PayAddressCode': grpc.unary_unary_rpc_method_handler(
          servicer.PayAddressCode,
          request_deserializer=mobilecoind__api__pb2.PayAddressCodeRequest.FromString,
          response_serializer=mobilecoind__api__pb2.SendPaymentResponse.SerializeToString,
      ),
      'GetNetworkStatus': grpc.unary_unary_rpc_method_handler(
          servicer.GetNetworkStatus,
          request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
          response_serializer=mobilecoind__api__pb2.GetNetworkStatusResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'mobilecoind_api.MobilecoindAPI', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
