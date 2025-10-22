                ('duration', models.DurationField(verbose_name='Продолжительность')),
                ('base_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Базовая цена')),
            ],
        ),
        migrations.CreateModel(
            name='Seat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('row', models.PositiveIntegerField(verbose_name='Ряд')),
                ('number', models.PositiveIntegerField(verbose_name='Номер')),
                ('category', models.CharField(choices=[('PARTERRE', 'Партер'), ('BALCONY', 'Балкон'), ('LOGE', 'Ложа')], max_length=20, verbose_name='Категория')),
                ('price_coefficient', models.DecimalField(decimal_places=2, max_digits=3, verbose_name='Коэффициент цены')),
            ],
            options={
                'unique_together': {('row', 'number')},
            },
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('FREE', 'Свободен'), ('BOOKED', 'Забронирован'), ('SOLD', 'Продан')], default='FREE', max_length=10, verbose_name='Статус')),
                ('reserved_until', models.DateTimeField(blank=True, null=True, verbose_name='Забронирован до')),
                ('reserved_by', models.CharField(blank=True, max_length=100, verbose_name='Забронировано (ID пользователя)')),
                ('performance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticket_manager.performance', verbose_name='Спектакль')),
                ('seat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticket_manager.seat', verbose_name='Место')),
            ],
        ),
    ]
