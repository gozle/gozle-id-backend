ChangeTypeChoices = (
    ('deposit', 'Deposit'),
    ('transfer', 'Transfer'),
    ('payment', 'Payment'),
)


class BalanceChange(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='balance_changes')

    type = models.CharField(max_length=20, choices=ChangeTypeChoices)
    amount = models.PositiveIntegerField()
    source = models.CharField(max_length=50, blank=True, null=True)

    verification_code = models.CharField(max_length=40, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
