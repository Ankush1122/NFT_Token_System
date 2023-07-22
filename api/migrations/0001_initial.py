# Generated by Django 4.2.3 on 2023-07-22 17:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Block',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.BigIntegerField()),
                ('merkleRoot', models.TextField()),
                ('previousHash', models.TextField(null=True)),
                ('difficulty', models.BigIntegerField()),
                ('nonce', models.BigIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='BlockChain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('difficulty', models.BigIntegerField()),
                ('trustedPublicKey', models.TextField()),
                ('blockSize', models.BigIntegerField()),
                ('coinToken', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='SmartContract',
            fields=[
                ('id', models.TextField(primary_key=True, serialize=False)),
                ('sellerPublicKey', models.TextField()),
                ('sellingAmount', models.BigIntegerField()),
                ('sellingToken', models.TextField()),
                ('buyerPublicKey', models.TextField()),
                ('buyingAmount', models.BigIntegerField()),
                ('buyingToken', models.TextField()),
                ('expiryDate', models.TextField()),
                ('physicalAsset', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('index', models.BigIntegerField(null=True)),
                ('transactionHash', models.TextField()),
                ('smartContract', models.TextField(null=True)),
                ('timeStamp', models.TextField()),
                ('parentBlock', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.block')),
            ],
        ),
        migrations.CreateModel(
            name='Output',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('index', models.BigIntegerField()),
                ('value', models.BigIntegerField()),
                ('token', models.TextField()),
                ('publicKey', models.TextField()),
                ('parentTransaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.transaction')),
            ],
        ),
        migrations.CreateModel(
            name='Input',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.BigIntegerField()),
                ('blockNumber', models.BigIntegerField()),
                ('TransactionHash', models.TextField()),
                ('outputIndex', models.BigIntegerField()),
                ('signature', models.TextField()),
                ('parentTransaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.transaction')),
            ],
        ),
    ]
