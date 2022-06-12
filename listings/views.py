from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from .models import Listing
from django.shortcuts import get_object_or_404
from listings.choices import price_choices, bedroom_choices, state_choices


def index(request):
    listings = Listing.objects.order_by('-list_date').filter(is_published=True)
    paginator = Paginator(listings, 3)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)

    context = {
        'listings': paged_listings,

    }
    return render(request, 'listings/listings.html', context)


def listing(request, listing_id):
    paged_listings = get_object_or_404(Listing, pk=listing_id)
    context = {
        'listing': paged_listings,
    }
    return render(request, 'listings/listing.html', context)


def search(request):
    queryset_list = Listing.objects.order_by('-list_date')

    # Keywords
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        queryset_list = queryset_list.filter(description__icontains=keywords)

    # City
    if 'city' in request.GET:
        city = request.GET['city']
        queryset_list = queryset_list.filter(city__icontains=city)

    # State
    if 'state' in request.GET:
        state = request.GET['state']
        queryset_list = queryset_list.filter(state__exact=state)

    # Bedrooms
    if 'bedrooms' in request.GET:
        bedrooms = request.GET['bedrooms']
        if int(bedrooms) == 0:
            queryset_list = queryset_list.filter(bedrooms__gte=bedrooms)
        else:
            queryset_list = queryset_list.filter(bedrooms__lte=bedrooms)

    # Price
    if 'price' in request.GET:
        price = request.GET['price']
        if int(price) == 0:
            queryset_list = queryset_list.filter(price__gte=price)
        else:
            queryset_list = queryset_list.filter(price__lte=price)

    context = {
        'state_choices': state_choices,
        'bedroom_choices': bedroom_choices,
        'price_choices': price_choices,
        'listings': queryset_list,
        'values': request.GET,
    }
    return render(request, 'listings/search.html', context)
