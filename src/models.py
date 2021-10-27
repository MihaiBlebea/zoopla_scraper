
class Listing():

	def __init__(
		self, 
		listing_id, 
		price,
		title,
		url,
		bath_count,
		bedroom_count,
		reception_count,
		address,
		phone,
		created = None):

		self.id = None
		self.listing_id = str(listing_id)
		self.price = price
		self.title = title
		self.url = url
		self.bath_count = bath_count
		self.bedroom_count = bedroom_count
		self.reception_count = reception_count
		self.address = address
		self.phone = phone
		self.created = created