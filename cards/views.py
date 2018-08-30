from ajson import ASerializer
from django.http import JsonResponse
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.viewsets import ViewSet

from cards.models import Card, UpdateCard


class ViewCards(ViewSet):
    permission_classes = [AllowAny]

    def list(self, request: Request):
        cards = Card.get_user_cards(request.user)
        return JsonResponse({
            "data": ASerializer().to_dict(list(cards), groups=['basic'])
        })

    def retrieve(self, request: Request, pk: str):
        card: Card = get_object_or_404(Card, pk=pk, user=request.user)
        return JsonResponse({
            "data": ASerializer().to_dict(card, groups=['detailed'])
        })

    def create(self, request: Request):
        card: Card = ASerializer().from_dict(request.data, Card)
        card.user = request.user
        card.save()
        return JsonResponse({
            "data": ASerializer().to_dict(card, groups=['detailed'])
        })

    def update(self, request: Request, pk: str):
        # make sure data has the right format
        card = ASerializer().from_dict(request.data, UpdateCard)
        card_data = ASerializer().to_dict(card, groups=["basic"])

        card: Card = get_object_or_404(Card, pk=pk, user=request.user)
        for key, value in card_data.items():
            setattr(card, key, value)
        card.save()
        return JsonResponse({
            "data": ASerializer().to_dict(card, groups=['detailed'])
        })
