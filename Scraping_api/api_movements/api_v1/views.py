from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from datetime import datetime

from api_v1.serializers import (
    BalanceSerializer,
    HoldingSerializer,
    BuySellMovementSerializer,
    DepositExtractionMovementSerializer,
    CredentialsSerializer,
    CompanySerializer,
)
from api_v1.models import (
    Balance,
    Holding,
    BuySellMovement,
    DepositExtractionMovement,
    Credentials,
    Company,
)
from Cocos import Cocos
from Driver import Driver
from Iol import Iol
from rest_framework.exceptions import NotFound


class CredentialsView(APIView):
    def post(self, request, company_id):
        serializer = CredentialsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(company_id=company_id)
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)



class UserCredentialsView(APIView):
    def get(self, request, company_id, user_id):
        credentials = get_object_or_404(Credentials, company_id=company_id, user_id=user_id)
        print(credentials.password)
        return Response({
            'username': credentials.username,
            'password': credentials.password,
        })

    def post(self, request, company_id, user_id):
        # Check if credentials already exist
        if Credentials.objects.filter(company_id=company_id, user_id=user_id).exists():
            return Response({'message': ' Credentials for this company have already been registered.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CredentialsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(company_id=company_id, user_id=user_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class BalanceView(APIView):
    def get(self, request, company_id, user_id):
        username = request.data.get('username')
        password = request.data.get('password')

        if username is None or password is None:
            return Response({'error': 'Invalid username or password'}, status=400)

        balance_instance = Balance.objects.filter(company_id=company_id, user_id=user_id).first()

        if balance_instance is None:
            # Initialize the required drivers and services
            driver = Driver()
            cocos = Cocos(driver, username, password)
            invertir_online = Iol(driver, username, password)

            if company_id == '1':
                balance_data = cocos.obtenerBalance()
            elif company_id == '2':
                balance_data = invertir_online.obtenerBalance()
            else:
                return Response({'error': 'Invalid balance ID'}, status=400)

            if balance_data is None:
                return Response({'error': 'Failed to obtain balance data'}, status=500)

            # Create a new balance instance in the database
            balance_instance = Balance.objects.create(
                company_id=company_id,
                user_id=user_id,
                balance=balance_data['Balance'],
                last_updated=datetime.now()
            )

        response_data = {
            'balance': balance_instance.balance,
            'last_updated': balance_instance.last_updated
        }

        return Response(response_data)



class UpdateBalanceView(APIView):
    def get(self, request, company_id, user_id):
        username = request.data.get('username')
        password = request.data.get('password')

        if username is None or password is None:
            return Response({'error': 'Invalid username or password'}, status=400)

        # Initialize the required drivers and services
        driver = Driver()
        cocos = Cocos(driver, username, password)
        invertir_online = Iol(driver, username, password)

        # Activate obtenerBalance for the required company
        if company_id == 1:
            balance_data = cocos.obtenerBalance()
        elif company_id == 2:
            balance_data = invertir_online.obtenerBalance()
        else:
            return Response({'error': 'Invalid balance ID'}, status=400)

        if balance_data is None:
            return Response({'error': 'Failed to obtain balance data'}, status=500)

        # Update the balance information in the database
        balance_instance = Balance.objects.filter(company_id=company_id, user_id=user_id).first()
        if balance_instance is not None:
            balance_instance.balance = balance_data['Balance']
            balance_instance.last_updated = datetime.now()
            balance_instance.save()

        response_data = {
            'balance': balance_data['Balance'],
            'last_updated': datetime.now()
        }

        return Response(response_data)
class HoldingView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        driver = Driver()
        cocos = Cocos(driver, username, password)
        holdings_data = cocos.obtenerHoldings()

        # Create a new instance of Holding model for each holding and save them
        for holding_data in holdings_data:
            holding_instance = Holding(
                ticker=holding_data['ticker'],
                variation=holding_data['variation'],
                price=holding_data['price'],
                quantity=holding_data['quantity'],
                amount=holding_data['amount']
            )
            holding_instance.save()

        serializer = HoldingSerializer(holdings_data, many=True)

        return Response(serializer.data)


class BuySellMovementView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        driver = Driver()
        cocos = Cocos(driver, username, password)
        buy_sell_movements_data = cocos.obtenerTodosMovimientos()

        # Create a new instance of BuySellMovement model for each movement and save them
        for movement_data in buy_sell_movements_data['BuySellMovements']:
            movement_instance = BuySellMovement(
                ticker=movement_data['ticker'],
                operation=movement_data['operation'],
                type=movement_data['type'],
                day=movement_data['day'],
                quantity=movement_data['quantity'],
                total_movement=movement_data['total_movement'],
                status=movement_data['status']
            )
            movement_instance.save()

        serializer = BuySellMovementSerializer(buy_sell_movements_data['BuySellMovements'], many=True)

        return Response(serializer.data)


class DepositExtractionMovementView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        driver = Driver()
        cocos = Cocos(driver, username, password)
        deposit_extraction_movements_data = cocos.obtenerTodosMovimientos()

        # Create a new instance of DepositExtractionMovement model for each movement and save them
        for movement_data in deposit_extraction_movements_data['DepositExtractionMovements']:
            movement_instance = DepositExtractionMovement(
                ticker=movement_data['ticker'],
                operation=movement_data['operation'],
                type=movement_data['type'],
                day=movement_data['day'],
                quantity=movement_data['quantity'],
                total_movement=movement_data['total_movement'],
                status=movement_data['status']
            )
            movement_instance.save()

        serializer = DepositExtractionMovementSerializer(deposit_extraction_movements_data['DepositExtractionMovements'], many=True)

        return Response(serializer.data)


class CompanyView(APIView):
    def get(self, request):
        companies = Company.objects.all()
        serializer = CompanySerializer(companies, many=True)
        return Response(serializer.data)


class CompanyCreationView(APIView):
    def post(self, request):
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class CompanyDetailView(APIView):
    def get(self, request, user_id):
        # Retrieve the credentials for the specified user_id
        credentials = Credentials.objects.filter(user_id=user_id)

        # Retrieve the companies associated with the credentials
        companies = Company.objects.filter(credentials__in=credentials)

        serializer = CompanySerializer(companies, many=True)
        return Response(serializer.data)


    def put(self, request, name):
        company = get_object_or_404(Company, name=name)
        serializer = CompanySerializer(company, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, name):
        company = get_object_or_404(Company, name=name)
        company.delete()
        return Response(status=204)
