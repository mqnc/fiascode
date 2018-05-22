
#include <initializer_list>

namespace {
	// A range which wraps a pair of iterators
	template<typename Iterator>
	class iterator_range {
	public:
		iterator_range(Iterator const& from, Iterator const& to) : mBegin(from), mEnd(to) {}
		bool empty() const { return mBegin == mEnd; }
		void popFront() { ++mBegin; } 		
		decltype(auto) front() const { return *mBegin; }
	private:
		Iterator mBegin;
		Iterator mEnd;
	};
}
 
template<typename Iterator>
iterator_range<Iterator> all(Iterator const& from, Iterator const& to) {
	return iterator_range<Iterator>(from, to);
}
 
template<typename Collection>
auto all(Collection& collection) {
	using std::begin;
	using std::end;
	return all(begin(collection), end(collection));
}
 
// Required because type deduction never deduces initializer_list.
template<typename T>
auto all(std::initializer_list<T> const& list) {
	return all(list.begin(), list.end());
}