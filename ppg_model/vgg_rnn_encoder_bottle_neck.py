from typing import Tuple

import numpy as np
import torch

from .e2e_asr_common import get_vgg2l_odim
from .nets_utils import make_pad_mask
from .encoders import RNN, RNNP, VGG2L
from nnsp.asr.encoder.abs_encoder import AbsEncoder


class VGGRNNBNEncoder(torch.nn.Module):
    """VGGRNNEncoder class with a bottle-neck layer.

    Args:
        input_size: The number of expected features in the input
        bidirectional: If ``True`` becomes a bidirectional LSTM
        use_projection: Use projection layer or not
        num_layers: Number of recurrent layers
        hidden_size: The number of hidden features
        output_size: The number of output features
        dropout: dropout probability

    """

    def __init__(
        self,
        input_size: int,
        rnn_type: str = "lstm",
        bidirectional: bool = True,
        use_projection: bool = True,
        num_layers: int = 4,
        hidden_size: int = 512,
        output_size: int = 512,  # projection dim if use_projection is True
        bottleneck_size: int = 256,
        dropout: float = 0.0,
        in_channel: int = 1,
        vgg_down_sample=True,
    ):
        super().__init__()
        self._output_size = output_size
        self.bottleneck_size = bottleneck_size
        self.rnn_type = rnn_type
        self.bidirectional = bidirectional
        self.use_projection = use_projection
        if rnn_type not in {"lstm", "gru"}:
            raise ValueError(f"Not supported rnn_type={rnn_type}")

        # Subsample is not used for VGGRNN
        subsample = np.ones(num_layers + 1, dtype=np.int)
        rnn_type = ("b" if bidirectional else "") + rnn_type
        if use_projection:
            self.enc = torch.nn.ModuleList(
                [
                    VGG2L(in_channel, vgg_down_sample),
                    RNNP(
                        get_vgg2l_odim(input_size, in_channel=in_channel, downsample=vgg_down_sample),
                        num_layers,
                        hidden_size,
                        output_size,
                        subsample,
                        dropout,
                        typ=rnn_type,
                    ),
                ]
            )

        else:
            self.enc = torch.nn.ModuleList(
                [
                    VGG2L(in_channel),
                    RNN(
                        get_vgg2l_odim(input_size, in_channel=in_channel, downsample=vgg_down_sample),
                        num_layers,
                        hidden_size,
                        output_size,
                        dropout,
                        typ=rnn_type,
                    ),
                ]
            )
        self.bottleneck_layer = torch.nn.Sequential(
            torch.nn.ReLU(),
            torch.nn.Linear(output_size, bottleneck_size),
        )

    def output_size(self) -> int:
        # return self._output_size
        return self.bottleneck_size

    def forward(
        self,
        xs_pad: torch.Tensor,
        ilens: torch.Tensor,
        prev_states: torch.Tensor = None,
    ) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        if prev_states is None:
            prev_states = [None] * len(self.enc)
        assert len(prev_states) == len(self.enc)

        current_states = []
        for module, prev_state in zip(self.enc, prev_states):
            xs_pad, ilens, states = module(xs_pad, ilens, prev_state=prev_state)
            current_states.append(states)

        if self.use_projection:
            xs_pad.masked_fill_(make_pad_mask(ilens, xs_pad, 1), 0.0)
        else:
            xs_pad = xs_pad.masked_fill(make_pad_mask(ilens, xs_pad, 1), 0.0)
        xs_pad = self.bottleneck_layer(xs_pad)

        return xs_pad, ilens, current_states
