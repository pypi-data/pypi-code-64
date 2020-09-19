# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from .. import _utilities, _tables
from . import outputs
from ._inputs import *

__all__ = ['Preset']


class Preset(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 audio: Optional[pulumi.Input[pulumi.InputType['PresetAudioArgs']]] = None,
                 audio_codec_options: Optional[pulumi.Input[pulumi.InputType['PresetAudioCodecOptionsArgs']]] = None,
                 container: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 thumbnails: Optional[pulumi.Input[pulumi.InputType['PresetThumbnailsArgs']]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 video: Optional[pulumi.Input[pulumi.InputType['PresetVideoArgs']]] = None,
                 video_codec_options: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 video_watermarks: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['PresetVideoWatermarkArgs']]]]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Provides an Elastic Transcoder preset resource.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        bar = aws.elastictranscoder.Preset("bar",
            audio=aws.elastictranscoder.PresetAudioArgs(
                audio_packing_mode="SingleTrack",
                bit_rate="96",
                channels="2",
                codec="AAC",
                sample_rate="44100",
            ),
            audio_codec_options=aws.elastictranscoder.PresetAudioCodecOptionsArgs(
                profile="AAC-LC",
            ),
            container="mp4",
            description="Sample Preset",
            thumbnails=aws.elastictranscoder.PresetThumbnailsArgs(
                format="png",
                interval="120",
                max_height="auto",
                max_width="auto",
                padding_policy="Pad",
                sizing_policy="Fit",
            ),
            video=aws.elastictranscoder.PresetVideoArgs(
                bit_rate="1600",
                codec="H.264",
                display_aspect_ratio="16:9",
                fixed_gop="false",
                frame_rate="auto",
                keyframes_max_dist="240",
                max_frame_rate="60",
                max_height="auto",
                max_width="auto",
                padding_policy="Pad",
                sizing_policy="Fit",
            ),
            video_codec_options={
                "ColorSpaceConversionMode": "None",
                "InterlacedMode": "Progressive",
                "Level": "2.2",
                "MaxReferenceFrames": "3",
                "Profile": "main",
            },
            video_watermarks=[aws.elastictranscoder.PresetVideoWatermarkArgs(
                horizontal_align="Right",
                horizontal_offset="10px",
                id="Test",
                max_height="20%",
                max_width="20%",
                opacity="55.5",
                sizing_policy="ShrinkToFit",
                target="Content",
                vertical_align="Bottom",
                vertical_offset="10px",
            )])
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['PresetAudioArgs']] audio: Audio parameters object (documented below).
        :param pulumi.Input[pulumi.InputType['PresetAudioCodecOptionsArgs']] audio_codec_options: Codec options for the audio parameters (documented below)
        :param pulumi.Input[str] container: The container type for the output file. Valid values are `flac`, `flv`, `fmp4`, `gif`, `mp3`, `mp4`, `mpg`, `mxf`, `oga`, `ogg`, `ts`, and `webm`.
        :param pulumi.Input[str] description: A description of the preset (maximum 255 characters)
        :param pulumi.Input[str] name: The name of the preset. (maximum 40 characters)
        :param pulumi.Input[pulumi.InputType['PresetThumbnailsArgs']] thumbnails: Thumbnail parameters object (documented below)
        :param pulumi.Input[pulumi.InputType['PresetVideoArgs']] video: Video parameters object (documented below)
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] video_codec_options: Codec options for the video parameters
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['PresetVideoWatermarkArgs']]]] video_watermarks: Watermark parameters for the video parameters (documented below)
        """
        if __name__ is not None:
            warnings.warn("explicit use of __name__ is deprecated", DeprecationWarning)
            resource_name = __name__
        if __opts__ is not None:
            warnings.warn("explicit use of __opts__ is deprecated, use 'opts' instead", DeprecationWarning)
            opts = __opts__
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = dict()

            __props__['audio'] = audio
            __props__['audio_codec_options'] = audio_codec_options
            if container is None:
                raise TypeError("Missing required property 'container'")
            __props__['container'] = container
            __props__['description'] = description
            __props__['name'] = name
            __props__['thumbnails'] = thumbnails
            __props__['type'] = type
            __props__['video'] = video
            __props__['video_codec_options'] = video_codec_options
            __props__['video_watermarks'] = video_watermarks
            __props__['arn'] = None
        super(Preset, __self__).__init__(
            'aws:elastictranscoder/preset:Preset',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            arn: Optional[pulumi.Input[str]] = None,
            audio: Optional[pulumi.Input[pulumi.InputType['PresetAudioArgs']]] = None,
            audio_codec_options: Optional[pulumi.Input[pulumi.InputType['PresetAudioCodecOptionsArgs']]] = None,
            container: Optional[pulumi.Input[str]] = None,
            description: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            thumbnails: Optional[pulumi.Input[pulumi.InputType['PresetThumbnailsArgs']]] = None,
            type: Optional[pulumi.Input[str]] = None,
            video: Optional[pulumi.Input[pulumi.InputType['PresetVideoArgs']]] = None,
            video_codec_options: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            video_watermarks: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['PresetVideoWatermarkArgs']]]]] = None) -> 'Preset':
        """
        Get an existing Preset resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['PresetAudioArgs']] audio: Audio parameters object (documented below).
        :param pulumi.Input[pulumi.InputType['PresetAudioCodecOptionsArgs']] audio_codec_options: Codec options for the audio parameters (documented below)
        :param pulumi.Input[str] container: The container type for the output file. Valid values are `flac`, `flv`, `fmp4`, `gif`, `mp3`, `mp4`, `mpg`, `mxf`, `oga`, `ogg`, `ts`, and `webm`.
        :param pulumi.Input[str] description: A description of the preset (maximum 255 characters)
        :param pulumi.Input[str] name: The name of the preset. (maximum 40 characters)
        :param pulumi.Input[pulumi.InputType['PresetThumbnailsArgs']] thumbnails: Thumbnail parameters object (documented below)
        :param pulumi.Input[pulumi.InputType['PresetVideoArgs']] video: Video parameters object (documented below)
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] video_codec_options: Codec options for the video parameters
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['PresetVideoWatermarkArgs']]]] video_watermarks: Watermark parameters for the video parameters (documented below)
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["arn"] = arn
        __props__["audio"] = audio
        __props__["audio_codec_options"] = audio_codec_options
        __props__["container"] = container
        __props__["description"] = description
        __props__["name"] = name
        __props__["thumbnails"] = thumbnails
        __props__["type"] = type
        __props__["video"] = video
        __props__["video_codec_options"] = video_codec_options
        __props__["video_watermarks"] = video_watermarks
        return Preset(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def audio(self) -> pulumi.Output[Optional['outputs.PresetAudio']]:
        """
        Audio parameters object (documented below).
        """
        return pulumi.get(self, "audio")

    @property
    @pulumi.getter(name="audioCodecOptions")
    def audio_codec_options(self) -> pulumi.Output[Optional['outputs.PresetAudioCodecOptions']]:
        """
        Codec options for the audio parameters (documented below)
        """
        return pulumi.get(self, "audio_codec_options")

    @property
    @pulumi.getter
    def container(self) -> pulumi.Output[str]:
        """
        The container type for the output file. Valid values are `flac`, `flv`, `fmp4`, `gif`, `mp3`, `mp4`, `mpg`, `mxf`, `oga`, `ogg`, `ts`, and `webm`.
        """
        return pulumi.get(self, "container")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        A description of the preset (maximum 255 characters)
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the preset. (maximum 40 characters)
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def thumbnails(self) -> pulumi.Output[Optional['outputs.PresetThumbnails']]:
        """
        Thumbnail parameters object (documented below)
        """
        return pulumi.get(self, "thumbnails")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def video(self) -> pulumi.Output[Optional['outputs.PresetVideo']]:
        """
        Video parameters object (documented below)
        """
        return pulumi.get(self, "video")

    @property
    @pulumi.getter(name="videoCodecOptions")
    def video_codec_options(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Codec options for the video parameters
        """
        return pulumi.get(self, "video_codec_options")

    @property
    @pulumi.getter(name="videoWatermarks")
    def video_watermarks(self) -> pulumi.Output[Optional[Sequence['outputs.PresetVideoWatermark']]]:
        """
        Watermark parameters for the video parameters (documented below)
        """
        return pulumi.get(self, "video_watermarks")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

