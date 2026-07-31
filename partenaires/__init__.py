from .cinetpay_payin import CinetpayPayinProcessor
from .cinetpay_payout import CinetpayPayoutProcessor
from .ombf_payin import OmbfPayinProcessor
from .ombf_payout import OmbfPayoutProcessor
from .bizao_payin import BizaoPayinProcessor
from .mtnci_payin import MtnciPayinProcessor
from .mtnci_payout import MtnciPayoutProcessor
from .waveci_payin import WaveciPayinProcessor
from .waveci_payout import WaveciPayoutProcessor
from .ifutur_payin import ifuturPayinProcessor
from .mtncm_payin import MtncmPayinProcessor
from .mtncm_payout import MtncmPayoutProcessor
from .ifutur_payout import IfuturPayoutProcessor
from .omci_payout import OmciPayoutProcessor
from .omci_payin import OmciPayinProcessor
from .moovci_payin import MoovciPayinProcessor
from .wavebf_payin import WavebfPayinProcessor
from .wavebf_payout import WavebfPayoutProcessor
from .wavesn_payin import WavesnPayinProcessor
from .wavesn_payout import WavesnPayoutProcessor


def get_processor(file_name, data_file, partner_file, reco_start=None, reco_end=None, reco_date=None):
    """
    reco_start / reco_end : plage de réconciliation (V1.1.2).
    reco_date : conservé pour compatibilité V1.1.1 (utilisé comme début=fin si fourni seul).
    """
    file_name = file_name.lower()

    # Compatibilité V1.1.1 : une seule date → plage d'un jour
    if reco_date is not None and reco_start is None and reco_end is None:
        reco_start = reco_date
        reco_end = reco_date

    def _make(cls):
        return cls(data_file, partner_file, reco_start=reco_start, reco_end=reco_end)

    if 'cinetpay' in file_name and 'payin' in file_name:
        return _make(CinetpayPayinProcessor)
    if 'cinetpay' in file_name and 'payout' in file_name:
        return _make(CinetpayPayoutProcessor)
    if 'ombf' in file_name and 'payin' in file_name:
        return _make(OmbfPayinProcessor)
    if 'ombf' in file_name and 'payout' in file_name:
        return _make(OmbfPayoutProcessor)
    if 'bizao' in file_name and 'payin' in file_name:
        return _make(BizaoPayinProcessor)
    if 'mtnci' in file_name and 'payin' in file_name:
        return _make(MtnciPayinProcessor)
    if 'mtnci' in file_name and 'payout' in file_name:
        return _make(MtnciPayoutProcessor)
    if 'waveci' in file_name and 'payin' in file_name:
        return _make(WaveciPayinProcessor)
    if 'waveci' in file_name and 'payout' in file_name:
        return _make(WaveciPayoutProcessor)
    if 'ifutur' in file_name and 'payin' in file_name:
        return _make(ifuturPayinProcessor)
    if 'mtncm' in file_name and 'payin' in file_name:
        return _make(MtncmPayinProcessor)
    if 'mtncm' in file_name and 'payout' in file_name:
        return _make(MtncmPayoutProcessor)
    if 'ifutur' in file_name and 'payout' in file_name:
        return _make(IfuturPayoutProcessor)
    if 'orangeci' in file_name and 'payout' in file_name:
        return _make(OmciPayoutProcessor)
    if 'orangeci' in file_name and 'payin' in file_name:
        return _make(OmciPayinProcessor)
    if 'moovci' in file_name and 'payin' in file_name:
        return _make(MoovciPayinProcessor)
    if 'wavebf' in file_name and 'payin' in file_name:
        return _make(WavebfPayinProcessor)
    if 'wavebf' in file_name and 'payout' in file_name:
        return _make(WavebfPayoutProcessor)
    if 'wavesn' in file_name and 'payin' in file_name:
        return _make(WavesnPayinProcessor)
    if 'wavesn' in file_name and 'payout' in file_name:
        return _make(WavesnPayoutProcessor)

    raise ValueError("Type de partenaire non reconnu")
