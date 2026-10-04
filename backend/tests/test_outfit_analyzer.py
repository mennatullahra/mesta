import pytest
from app.services.ai.base import AIProvider
from app.services.ai.outfit_analyzer import OutfitAnalyzer, InvalidAIOutputError

VALID={"overall_style":["elegant"],"occasion":[],"dominant_colors":["burgundy"],"items":[{"category":"blouse","color":"burgundy","color_family":"red","confidence":0.9}]}
class Fake(AIProvider):
    def __init__(self,responses): self.responses=list(responses); self.calls=0
    def analyze_outfit(self,*args,**kwargs): self.calls+=1; return self.responses.pop(0)

def test_valid_ai_output():
    a=OutfitAnalyzer(Fake([VALID])).analyze(b"abc","image/jpeg")
    assert a.items[0].category=="blouse"

def test_invalid_retries_once_then_succeeds():
    f=Fake([{"items":[]},VALID]); a=OutfitAnalyzer(f).analyze(b"abc","image/jpeg")
    assert f.calls==2 and a.items

def test_invalid_twice_fails_gracefully():
    f=Fake([{"items":[]},{"items":[]}])
    with pytest.raises(InvalidAIOutputError): OutfitAnalyzer(f).analyze(b"abc","image/jpeg")

def test_cache_avoids_second_ai_call():
    f=Fake([VALID]); a=OutfitAnalyzer(f); a.analyze(b"same","image/jpeg"); a.analyze(b"same","image/jpeg")
    assert f.calls==1
