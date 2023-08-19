from django.shortcuts import render

from .forms import ManufacturerForm
from .models import Manufacturer, Model, Car


def index(request):
    if request.htmx:
        model = request.GET.get('model')
        manufacturer = request.GET.get('manufacturers')
        try:
            manufacturer = int(request.GET.get('manufacturers'))
        except (ValueError, TypeError):
            if manufacturer:
                manufacturer = Manufacturer.objects.create(name=request.GET.get('manufacturers')).id

        try:
            model = int(model)
        except (ValueError, TypeError):
            if model:
                model = Model.objects.create(name=model, manufacturer_id=manufacturer).id

        dic = {
            'model': model,
            'manufacturers': manufacturer}
        form = ManufacturerForm(dic)
        return render(request, 'core/form.html', {
            'form': form,
        })

    form = ManufacturerForm()
    cars = Car.objects.all()

    return render(request, 'core/index.html', {
        'form': form,
        'cars': cars,
    })


def add(request):
    if request.htmx:
        form = ManufacturerForm(request.POST)
        manufacturer = Manufacturer.objects.get(id=form['manufacturers'].value())
        model = Model.objects.get(id=form['model'].value())
        instance = Car.objects.create(
            manufacturer=manufacturer,
            model=model,
            price=form['price'].value(),
        )

        return render(request, 'partials/list-item.html', {
            'car': instance,
        })
