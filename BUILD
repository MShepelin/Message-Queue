load("//bazel:python_rules.bzl", "py_grpc_library", "py_proto_library")

licenses(["notice"])

package(default_visibility = ["//visibility:public"])

py_proto_library(
    name = "wikilength_py_pb2",
    deps = [":wikilength_proto"],
)

py_grpc_library(
    name = "wikilength_py_pb2_grpc",
    srcs = [":wikilength_proto"],
    deps = [":wikilength_py_pb2"],
)
