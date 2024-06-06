// compatibility_fixes.hpp
#pragma once

#include <type_traits> // For standard type traits
#include <utility>     // For std::declval

// Conditional mimicry of std::underlying_type for compilers that lack it.
#if !defined(__GNUC__) || __GNUC__ < 4 || (__GNUC__ == 4 && __GNUC_MINOR__ < 7)
namespace std {

template<typename _Tp>
class underlying_type {
public:
    // This workaround lacks a true implementation because __underlying_type is compiler-specific and not portable.
    // As such, this is a placeholder to prevent compilation errors, but it won't provide a working implementation.
    typedef typename _Tp::type type; // Placeholder, incorrect but prevents compilation errors.
};

} // namespace std
#endif

// Conditional implementation for std::is_nothrow_move_constructible, relying on is_nothrow_constructible as a fallback.
#if !defined(__GNUC__) || __GNUC__ < 4 || (__GNUC__ == 4 && __GNUC_MINOR__ < 7)
namespace std {

template<class T>
struct is_nothrow_move_constructible : public is_nothrow_constructible<T, T&&> {};

} // namespace std
#endif

// std::is_trivially_destructible fallback.
#if !defined(__GNUC__) || __GNUC__ < 4 || (__GNUC__ == 4 && __GNUC_MINOR__ < 7)
namespace std {

template<class T>
struct is_trivially_destructible : public has_trivial_destructor<T> {};

} // namespace std
#endif

// Fallback for std::is_assignable, simplified version.
#if !defined(__GNUC__) || __GNUC__ < 4 || (__GNUC__ == 4 && __GNUC_MINOR__ < 7)
namespace std {

template<typename _Tp, typename _Up>
    class __is_assignable_helper
    {
      template<typename _Tp1, typename _Up1,
	       typename = decltype(declval<_Tp1>() = declval<_Up1>())>
	static true_type
	__test(int);

      template<typename, typename>
	static false_type
	__test(...);

    public:
      typedef decltype(__test<_Tp, _Up>(0)) type;
    };

/// is_assignable
template<typename _Tp, typename _Up>
    struct is_assignable
      : public __is_assignable_helper<_Tp, _Up>::type
    { };

} // namespace std
#endif
