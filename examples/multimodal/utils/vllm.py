# SPDX-FileCopyrightText: Copyright (c) 2025 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# TODO: rename to avoid ambiguity with vllm package
from vllm.engine.arg_utils import AsyncEngineArgs
from vllm.utils import FlexibleArgumentParser

from dynamo.sdk.lib.config import ServiceConfig


def parse_vllm_args(service_name, prefix) -> AsyncEngineArgs:
    config = ServiceConfig.get_instance()
    vllm_args = config.as_args(service_name, prefix=prefix)
    parser = FlexibleArgumentParser()
    parser.add_argument(
        "--router",
        type=str,
        choices=["random", "round-robin", "kv"],
        default="random",
        help="Router type to use for scheduling requests to workers",
    )
    parser.add_argument(
        "--remote-prefill", action="store_true", help="Enable remote prefill"
    )
    parser.add_argument(
        "--conditional-disagg",
        action="store_true",
        help="Use disaggregated router to decide whether to prefill locally or remotely",
    )
    parser.add_argument(
        "--max-local-prefill-length",
        type=int,
        default=1000,
        help="Maximum length for local prefill. If remote prefill is enabled and the prefill length is greater than this value the request will be sent for remote prefill, otherwise prefill phase will run locally.",
    )
    parser.add_argument(
        "--max-prefill-queue-size",
        type=int,
        default=3,
        help="Maximum queue size for remote prefill. If the prefill queue size is greater than this value, prefill phase of the incoming request will be executed locally.",
    )
    parser.add_argument(
        "--image-token-id",
        type=int,
        default=32000,
        help="Image token ID used to represent image patches in the token sequence",
    )
    parser.add_argument(
        "--num-patches",
        type=int,
        default=576,
        help="Number of patches the input image is divided into (must be positive)",
    )
    parser.add_argument(
        "--prompt-template",
        type=str,
        default="<prompt>",
        help="Prompt template to use for the model",
    )
    parser.add_argument(
        "--num-sampled-frames",
        type=int,
        default=8,
        help="Number of frames to sample from the video",
    )
    parser.add_argument(
        "--frame-height",
        type=int,
        default=336,
        help="Height of the video frames",
    )
    parser.add_argument(
        "--frame-width",
        type=int,
        default=336,
        help="Width of the video frames",
    )
    parser.add_argument(
        "--frame-channels",
        type=int,
        default=3,
        help="Number of channels in the video frames",
    )
    parser.add_argument(
        "--dummy-token-id",
        type=int,
        default=0,
        help="Dummy token ID",
    )
    parser.add_argument(
        "--video-token-id",
        type=int,
        default=32000,
        help="Video token ID",
    )
    parser.add_argument(
        "--dummy-tokens-per-frame",
        type=int,
        default=144,
        help="Number of dummy tokens per frame",
    )
    parser = AsyncEngineArgs.add_cli_args(parser)
    args = parser.parse_args(vllm_args)
    engine_args = AsyncEngineArgs.from_cli_args(args)
    engine_args.router = args.router
    engine_args.remote_prefill = args.remote_prefill
    engine_args.conditional_disagg = args.conditional_disagg
    engine_args.max_local_prefill_length = args.max_local_prefill_length
    engine_args.max_prefill_queue_size = args.max_prefill_queue_size
    engine_args.prompt_template = args.prompt_template
    engine_args.num_sampled_frames = args.num_sampled_frames
    engine_args.frame_height = args.frame_height
    engine_args.frame_width = args.frame_width
    engine_args.frame_channels = args.frame_channels
    engine_args.dummy_token_id = args.dummy_token_id
    engine_args.video_token_id = args.video_token_id
    engine_args.dummy_tokens_per_frame = args.dummy_tokens_per_frame
    engine_args.num_patches = args.num_patches
    engine_args.image_token_id = args.image_token_id
    return engine_args
