import os

from pytest_mock import MockFixture

from opta.layer import Layer
from opta.module_processors.aws_cloudfront_distribution import (
    AwsCloudfrontDstributionProcessor,
)


class TestAwsCloudfrontDstributionProcessor:
    def test_all_good(self, mocker: MockFixture) -> None:
        layer = Layer.load_from_yaml(
            os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                "module_processors",
                "dummy_config1.yaml",
            ),
            None,
        )
        idx = len(layer.modules)
        cloudfront_module = layer.get_module("cloudfront", idx)
        assert cloudfront_module is not None
        AwsCloudfrontDstributionProcessor(cloudfront_module, layer).process(idx)
        assert cloudfront_module.data["bucket_name"] == "${{module.bucket1.bucket_id}}"
        assert (
            cloudfront_module.data["origin_access_identity_path"]
            == "${{module.bucket1.cloudfront_read_path}}"
        )