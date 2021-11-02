from django.test import TestCase
from restapi import models
from django.urls import reverse

# Create your tests here.


class TestModels(TestCase):
    def test_expense(self):
        expense = models.Expense.objects.create(
            amount=249.99,
            merchant="Amazon",
            description="ANC headphones",
            category="music",
        )
        inserted_expense = models.Expense.objects.get(pk=expense.id)

        self.assertEqual(249.99, inserted_expense.amount)
        self.assertEqual("Amazon", inserted_expense.merchant)
        self.assertEqual("ANC headphones", inserted_expense.description)
        self.assertEqual("music", inserted_expense.category)


class TestViews(TestCase):
    def test_expense_create(self):
        payload = {
            "amount": 50.0,
            "merchant": "atnt",
            "description": "cellphone subscription",
            "category": "utilities",
        }
        res = self.client.post(
            reverse("restapi:expense-list-create"), payload, format="json"
        )

        self.assertEqual(201, res.status_code)

        json_res = res.json()
        self.assertEqual(payload["amount"], json_res["amount"])
        self.assertEqual(payload["merchant"], json_res["merchant"])
        self.assertEqual(payload["description"], json_res["description"])
        self.assertEqual(payload["category"], json_res["category"])

        self.assertIsInstance(json_res["id"], int)

    def test_expense_list(self):
        res = self.client.get(reverse("restapi:expense-list-create"), format="json")
        self.assertEqual(200, res.status_code)
        json_res = res.json()
        self.assertIsInstance(json_res, list)
        expenses = models.Expense.objects.all()
        self.assertEqual(len(expenses), len(json_res))

    def test_required_fields_missing(self):
        payload = {
            "merchant": "atnt",
            "description": "cellphone subscription",
            "category": "utilities",
        }
        res = self.client.post(
            reverse("restapi:expense-list-create"), payload, format="json"
        )
        self.assertEqual(400, res.status_code)

    def test_retrieve(self):
        expense = models.Expense.objects.create(
            amount=300, merchant="George", description="loan", category="transfer"
        )
        res = self.client.get(
            reverse("restapi:expense-retrieve-delete", args=[expense.id]), format="json"
        )

        self.assertEqual(200, res.status_code)

        json_res = res.json()
        self.assertEqual(expense.id, json_res["id"])
        self.assertEqual(expense.amount, json_res["amount"])
        self.assertEqual(expense.merchant, json_res["merchant"])
        self.assertEqual(expense.description, json_res["description"])
        self.assertEqual(expense.category, json_res["category"])

    def test_delete(self):
        expense = models.Expense.objects.create(
            amount=50, merchant="John", description="loan", category="transfer"
        )
        res = self.client.delete(
            reverse("restapi:expense-retrieve-delete", args=[expense.id]), format="json"
        )

        self.assertEqual(204, res.status_code)
        self.assertFalse(models.Expense.objects.filter(pk=expense.id).exists())

    def test_filter_by_merchnt(self):
        amazon_expense = models.Expense.objects.create(
            amount=1000, merchant="amazon", description="sunglasses", category="fashion"
        )
        ebay_expense = models.Expense.objects.create(
            amount=2000, merchant="ebay", description="watch", category="fashion"
        )

        url = "/api/expenses?merchant=amazon"
        res = self.client.get(url, format="json")

        self.assertEqual(200, res.status_code)
        json_res = res.json()
        self.assertEqual(1, len(json_res))
        self.assertEqual(amazon_expense.id, json_res[0]["id"])
        self.assertEqual(amazon_expense.merchant, json_res[0]["merchant"])
        self.assertEqual(amazon_expense.amount, json_res[0]["amount"])
        self.assertEqual(amazon_expense.description, json_res[0]["description"])
        self.assertEqual(amazon_expense.category, json_res[0]["category"])
