
namespace
{
	// An iterable which wraps a pair of iterators.
	template<typename Iterator>
	class iterator_range {
	public:
		iterator_range(Iterator const& from, Iterator const& to)
		: mBegin(from)
		, mEnd(to)
		{}
 
		bool empty() const {
			return mBegin == mEnd;
		}
 
		auto front() const {
			return *mBegin;
		}
 
		void popFront() {
			++mBegin;
		}
 
		friend Iterator const& begin(iterator_range const& rng) {
			return rng.mBegin;
		}
 
		friend Iterator const& end(iterator_range const& rng) {
			return rng.mEnd;
		}
 
	private:
		Iterator mBegin;
		Iterator mEnd;
	};
}

template<typename Iterator>
iterator_range<Iterator>
make_range(Iterator const& from, Iterator const& to) {
	return iterator_range<Iterator>(from, to);
}
 
template<typename Collection>
auto all(Collection& collection) {
	using std::begin;
	using std::end;
	return make_range(begin(collection), end(collection));
}
 
// Required because type deduction never deduces initializer_list.	
template<typename T>
auto all(std::initializer_list<T> const& list) {
	return make_range(list.begin(), list.end());
}
