from Auth.models import PhoneVerification
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST

from .forms import SellBookForm
from .models import Book, PhoneNumberRequest
from .utils import update_pinecone_index, co, index


@login_required
def book_list(request):
    query = request.GET.get('query', '')
    if query:
        query_embedding = co.embed(texts=[query], model="embed-english-v2.0").embeddings[0]
        result = index.query(vector=query_embedding, top_k=3)

        book_data = [{'id': match['id'], 'score': match['score']} for match in result['matches']]

        book_order = {int(data['id']): data['score'] for data in book_data}
        books = list(Book.objects.filter(id__in=book_order.keys(), is_sold=False))
        books_sorted = sorted(books, key=lambda book: book_order.get(book.id, 0), reverse=True)


    else:
        books_sorted = Book.objects.filter(is_sold=False)

    return render(request, 'book_list.html', {'books': books_sorted})


@login_required
def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    try:
        phone_verification = PhoneVerification.objects.get(username=book.owner.username)
        seller_phone_number = phone_verification.phone_number
    except PhoneVerification.DoesNotExist:
        seller_phone_number = 'Phone number not found'
    return render(request, 'book_detail.html', {'book': book, 'seller_phone_number': seller_phone_number})


@login_required
def sell_book(request):
    if request.method == 'POST':
        form = SellBookForm(request.POST, request.FILES)
        if form.is_valid():
            book = Book.objects.create(
                title=form.cleaned_data['title'],
                author=form.cleaned_data['author'],
                description=form.cleaned_data['description'],
                price=form.cleaned_data['price'],
                image=form.cleaned_data['image'],
                owner=request.user,
                is_sold=form.cleaned_data['is_sold']
            )
            book.save()
            # Update the Pinecone index with the new book
            update_pinecone_index(book)
            return redirect('book_list')
    else:
        form = SellBookForm()
    return render(request, 'sell_book.html', {'form': form})


@require_POST
@login_required
def request_phone_number(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    try:
        phone_verification = PhoneVerification.objects.get(username=book.owner.username)
        phone_number = phone_verification.phone_number
        PhoneNumberRequest.objects.create(book=book, viewer=request.user)  # Store the request
        return JsonResponse({'phone_number': phone_number})
    except PhoneVerification.DoesNotExist:
        return JsonResponse({'error': 'Phone number not found'}, status=404)


@login_required
def user_books(request):
    books = Book.objects.filter(owner=request.user, is_sold=False)
    for book in books:
        phone_requests = PhoneNumberRequest.objects.filter(book=book)
        for phone_request in phone_requests:
            try:
                phone_verification = PhoneVerification.objects.get(username=phone_request.viewer.username)
                phone_request.phone_number = phone_verification.phone_number
            except PhoneVerification.DoesNotExist:
                phone_request.phone_number = 'Not Available'
        book.phone_requests = phone_requests
    return render(request, 'user_books.html', {'books': books})


@login_required
def view_cart(request):
    # Retrieve all phone number requests made by the current user
    try:
        phone_requests = PhoneNumberRequest.objects.filter(viewer=request.user)

        # Gather book information from the phone requests
        books_requested = [phone_request.book for phone_request in phone_requests]
        # print(type(books_requested[0]))
        return render(request, 'view_cart.html', {'books': books_requested})
    except:
        return render(request, 'view_cart.html', {'books': []})


# For general use
# @login_required
# def user_books(request):
#     books = Book.objects.filter(owner=request.user, is_sold=False)
#     return render(request, 'user_books.html', {'books': books})


@login_required
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id, owner=request.user)
    if request.method == 'POST':
        form = SellBookForm(request.POST, request.FILES)
        if form.is_valid():
            book.title = form.cleaned_data['title']
            book.author = form.cleaned_data['author']
            book.description = form.cleaned_data['description']
            book.price = form.cleaned_data['price']
            if 'image' in request.FILES:
                book.image = request.FILES['image']
            book.is_sold = form.cleaned_data['is_sold']
            book.save()
            return redirect('user_books')
    else:
        form = SellBookForm(initial={
            'title': book.title,
            'author': book.author,
            'description': book.description,
            'price': book.price,
            'is_sold': book.is_sold,
        })
    return render(request, 'edit_book.html', {'form': form, 'book': book})


@login_required
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id, owner=request.user)
    if request.method == 'POST':
        book.delete()
        return redirect('user_books')
    return render(request, 'delete_book.html', {'book': book})
