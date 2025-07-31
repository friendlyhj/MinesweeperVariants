(function () {
    const t = document.createElement("link").relList;
    if (t && t.supports && t.supports("modulepreload")) return;
    for (const r of document.querySelectorAll('link[rel="modulepreload"]')) n(r);
    new MutationObserver(r => {
        for (const l of r) if (l.type === "childList") for (const o of l.addedNodes) o.tagName === "LINK" && o.rel === "modulepreload" && n(o)
    }).observe(document, {childList: !0, subtree: !0});

    function s(r) {
        const l = {};
        return r.integrity && (l.integrity = r.integrity), r.referrerPolicy && (l.referrerPolicy = r.referrerPolicy), r.crossOrigin === "use-credentials" ? l.credentials = "include" : r.crossOrigin === "anonymous" ? l.credentials = "omit" : l.credentials = "same-origin", l
    }

    function n(r) {
        if (r.ep) return;
        r.ep = !0;
        const l = s(r);
        fetch(r.href, l)
    }
})();/**
 * @vue/shared v3.5.18
 * (c) 2018-present Yuxi (Evan) You and Vue contributors
 * @license MIT
 **//*! #__NO_SIDE_EFFECTS__ */
function Ks(e) {
    const t = Object.create(null);
    for (const s of e.split(",")) t[s] = 1;
    return s => s in t
}

const z = {}, ut = [], Le = () => {
    }, tl = () => !1,
    os = e => e.charCodeAt(0) === 111 && e.charCodeAt(1) === 110 && (e.charCodeAt(2) > 122 || e.charCodeAt(2) < 97),
    Vs = e => e.startsWith("onUpdate:"), de = Object.assign, Us = (e, t) => {
        const s = e.indexOf(t);
        s > -1 && e.splice(s, 1)
    }, sl = Object.prototype.hasOwnProperty, B = (e, t) => sl.call(e, t), I = Array.isArray,
    dt = e => is(e) === "[object Map]", Un = e => is(e) === "[object Set]", P = e => typeof e == "function",
    te = e => typeof e == "string", qe = e => typeof e == "symbol", X = e => e !== null && typeof e == "object",
    Gn = e => (X(e) || P(e)) && P(e.then) && P(e.catch), Wn = Object.prototype.toString, is = e => Wn.call(e),
    nl = e => is(e).slice(8, -1), qn = e => is(e) === "[object Object]",
    Gs = e => te(e) && e !== "NaN" && e[0] !== "-" && "" + parseInt(e, 10) === e,
    Tt = Ks(",key,ref,ref_for,ref_key,onVnodeBeforeMount,onVnodeMounted,onVnodeBeforeUpdate,onVnodeUpdated,onVnodeBeforeUnmount,onVnodeUnmounted"),
    cs = e => {
        const t = Object.create(null);
        return s => t[s] || (t[s] = e(s))
    }, rl = /-(\w)/g, Ze = cs(e => e.replace(rl, (t, s) => s ? s.toUpperCase() : "")), ll = /\B([A-Z])/g,
    ct = cs(e => e.replace(ll, "-$1").toLowerCase()), zn = cs(e => e.charAt(0).toUpperCase() + e.slice(1)),
    ys = cs(e => e ? `on${zn(e)}` : ""), Xe = (e, t) => !Object.is(e, t), bs = (e, ...t) => {
        for (let s = 0; s < e.length; s++) e[s](...t)
    }, Rs = (e, t, s, n = !1) => {
        Object.defineProperty(e, t, {configurable: !0, enumerable: !1, writable: n, value: s})
    }, ol = e => {
        const t = parseFloat(e);
        return isNaN(t) ? e : t
    };
let pn;
const fs = () => pn || (pn = typeof globalThis < "u" ? globalThis : typeof self < "u" ? self : typeof window < "u" ? window : typeof global < "u" ? global : {});

function Ws(e) {
    if (I(e)) {
        const t = {};
        for (let s = 0; s < e.length; s++) {
            const n = e[s], r = te(n) ? al(n) : Ws(n);
            if (r) for (const l in r) t[l] = r[l]
        }
        return t
    } else if (te(e) || X(e)) return e
}

const il = /;(?![^(]*\))/g, cl = /:([^]+)/, fl = /\/\*[^]*?\*\//g;

function al(e) {
    const t = {};
    return e.replace(fl, "").split(il).forEach(s => {
        if (s) {
            const n = s.split(cl);
            n.length > 1 && (t[n[0].trim()] = n[1].trim())
        }
    }), t
}

function as(e) {
    let t = "";
    if (te(e)) t = e; else if (I(e)) for (let s = 0; s < e.length; s++) {
        const n = as(e[s]);
        n && (t += n + " ")
    } else if (X(e)) for (const s in e) e[s] && (t += s + " ");
    return t.trim()
}

const ul = "itemscope,allowfullscreen,formnovalidate,ismap,nomodule,novalidate,readonly", dl = Ks(ul);

function Jn(e) {
    return !!e || e === ""
}

const Yn = e => !!(e && e.__v_isRef === !0),
    Te = e => te(e) ? e : e == null ? "" : I(e) || X(e) && (e.toString === Wn || !P(e.toString)) ? Yn(e) ? Te(e.value) : JSON.stringify(e, Qn, 2) : String(e),
    Qn = (e, t) => Yn(t) ? Qn(e, t.value) : dt(t) ? {[`Map(${t.size})`]: [...t.entries()].reduce((s, [n, r], l) => (s[Cs(n, l) + " =>"] = r, s), {})} : Un(t) ? {[`Set(${t.size})`]: [...t.values()].map(s => Cs(s))} : qe(t) ? Cs(t) : X(t) && !I(t) && !qn(t) ? String(t) : t,
    Cs = (e, t = "") => {
        var s;
        return qe(e) ? `Symbol(${(s = e.description) != null ? s : t})` : e
    };
/**
 * @vue/reactivity v3.5.18
 * (c) 2018-present Yuxi (Evan) You and Vue contributors
 * @license MIT
 **/let be;

class hl {
    constructor(t = !1) {
        this.detached = t, this._active = !0, this._on = 0, this.effects = [], this.cleanups = [], this._isPaused = !1, this.parent = be, !t && be && (this.index = (be.scopes || (be.scopes = [])).push(this) - 1)
    }

    get active() {
        return this._active
    }

    pause() {
        if (this._active) {
            this._isPaused = !0;
            let t, s;
            if (this.scopes) for (t = 0, s = this.scopes.length; t < s; t++) this.scopes[t].pause();
            for (t = 0, s = this.effects.length; t < s; t++) this.effects[t].pause()
        }
    }

    resume() {
        if (this._active && this._isPaused) {
            this._isPaused = !1;
            let t, s;
            if (this.scopes) for (t = 0, s = this.scopes.length; t < s; t++) this.scopes[t].resume();
            for (t = 0, s = this.effects.length; t < s; t++) this.effects[t].resume()
        }
    }

    run(t) {
        if (this._active) {
            const s = be;
            try {
                return be = this, t()
            } finally {
                be = s
            }
        }
    }

    on() {
        ++this._on === 1 && (this.prevScope = be, be = this)
    }

    off() {
        this._on > 0 && --this._on === 0 && (be = this.prevScope, this.prevScope = void 0)
    }

    stop(t) {
        if (this._active) {
            this._active = !1;
            let s, n;
            for (s = 0, n = this.effects.length; s < n; s++) this.effects[s].stop();
            for (this.effects.length = 0, s = 0, n = this.cleanups.length; s < n; s++) this.cleanups[s]();
            if (this.cleanups.length = 0, this.scopes) {
                for (s = 0, n = this.scopes.length; s < n; s++) this.scopes[s].stop(!0);
                this.scopes.length = 0
            }
            if (!this.detached && this.parent && !t) {
                const r = this.parent.scopes.pop();
                r && r !== this && (this.parent.scopes[this.index] = r, r.index = this.index)
            }
            this.parent = void 0
        }
    }
}

function pl() {
    return be
}

let q;
const ws = new WeakSet;

class Xn {
    constructor(t) {
        this.fn = t, this.deps = void 0, this.depsTail = void 0, this.flags = 5, this.next = void 0, this.cleanup = void 0, this.scheduler = void 0, be && be.active && be.effects.push(this)
    }

    pause() {
        this.flags |= 64
    }

    resume() {
        this.flags & 64 && (this.flags &= -65, ws.has(this) && (ws.delete(this), this.trigger()))
    }

    notify() {
        this.flags & 2 && !(this.flags & 32) || this.flags & 8 || er(this)
    }

    run() {
        if (!(this.flags & 1)) return this.fn();
        this.flags |= 2, gn(this), tr(this);
        const t = q, s = Oe;
        q = this, Oe = !0;
        try {
            return this.fn()
        } finally {
            sr(this), q = t, Oe = s, this.flags &= -3
        }
    }

    stop() {
        if (this.flags & 1) {
            for (let t = this.deps; t; t = t.nextDep) Js(t);
            this.deps = this.depsTail = void 0, gn(this), this.onStop && this.onStop(), this.flags &= -2
        }
    }

    trigger() {
        this.flags & 64 ? ws.add(this) : this.scheduler ? this.scheduler() : this.runIfDirty()
    }

    runIfDirty() {
        $s(this) && this.run()
    }

    get dirty() {
        return $s(this)
    }
}

let Zn = 0, St, Et;

function er(e, t = !1) {
    if (e.flags |= 8, t) {
        e.next = Et, Et = e;
        return
    }
    e.next = St, St = e
}

function qs() {
    Zn++
}

function zs() {
    if (--Zn > 0) return;
    if (Et) {
        let t = Et;
        for (Et = void 0; t;) {
            const s = t.next;
            t.next = void 0, t.flags &= -9, t = s
        }
    }
    let e;
    for (; St;) {
        let t = St;
        for (St = void 0; t;) {
            const s = t.next;
            if (t.next = void 0, t.flags &= -9, t.flags & 1) try {
                t.trigger()
            } catch (n) {
                e || (e = n)
            }
            t = s
        }
    }
    if (e) throw e
}

function tr(e) {
    for (let t = e.deps; t; t = t.nextDep) t.version = -1, t.prevActiveLink = t.dep.activeLink, t.dep.activeLink = t
}

function sr(e) {
    let t, s = e.depsTail, n = s;
    for (; n;) {
        const r = n.prevDep;
        n.version === -1 ? (n === s && (s = r), Js(n), gl(n)) : t = n, n.dep.activeLink = n.prevActiveLink, n.prevActiveLink = void 0, n = r
    }
    e.deps = t, e.depsTail = s
}

function $s(e) {
    for (let t = e.deps; t; t = t.nextDep) if (t.dep.version !== t.version || t.dep.computed && (nr(t.dep.computed) || t.dep.version !== t.version)) return !0;
    return !!e._dirty
}

function nr(e) {
    if (e.flags & 4 && !(e.flags & 16) || (e.flags &= -17, e.globalVersion === It) || (e.globalVersion = It, !e.isSSR && e.flags & 128 && (!e.deps && !e._dirty || !$s(e)))) return;
    e.flags |= 2;
    const t = e.dep, s = q, n = Oe;
    q = e, Oe = !0;
    try {
        tr(e);
        const r = e.fn(e._value);
        (t.version === 0 || Xe(r, e._value)) && (e.flags |= 128, e._value = r, t.version++)
    } catch (r) {
        throw t.version++, r
    } finally {
        q = s, Oe = n, sr(e), e.flags &= -3
    }
}

function Js(e, t = !1) {
    const {dep: s, prevSub: n, nextSub: r} = e;
    if (n && (n.nextSub = r, e.prevSub = void 0), r && (r.prevSub = n, e.nextSub = void 0), s.subs === e && (s.subs = n, !n && s.computed)) {
        s.computed.flags &= -5;
        for (let l = s.computed.deps; l; l = l.nextDep) Js(l, !0)
    }
    !t && !--s.sc && s.map && s.map.delete(s.key)
}

function gl(e) {
    const {prevDep: t, nextDep: s} = e;
    t && (t.nextDep = s, e.prevDep = void 0), s && (s.prevDep = t, e.nextDep = void 0)
}

let Oe = !0;
const rr = [];

function Ue() {
    rr.push(Oe), Oe = !1
}

function Ge() {
    const e = rr.pop();
    Oe = e === void 0 ? !0 : e
}

function gn(e) {
    const {cleanup: t} = e;
    if (e.cleanup = void 0, t) {
        const s = q;
        q = void 0;
        try {
            t()
        } finally {
            q = s
        }
    }
}

let It = 0;

class ml {
    constructor(t, s) {
        this.sub = t, this.dep = s, this.version = s.version, this.nextDep = this.prevDep = this.nextSub = this.prevSub = this.prevActiveLink = void 0
    }
}

class Ys {
    constructor(t) {
        this.computed = t, this.version = 0, this.activeLink = void 0, this.subs = void 0, this.map = void 0, this.key = void 0, this.sc = 0, this.__v_skip = !0
    }

    track(t) {
        if (!q || !Oe || q === this.computed) return;
        let s = this.activeLink;
        if (s === void 0 || s.sub !== q) s = this.activeLink = new ml(q, this), q.deps ? (s.prevDep = q.depsTail, q.depsTail.nextDep = s, q.depsTail = s) : q.deps = q.depsTail = s, lr(s); else if (s.version === -1 && (s.version = this.version, s.nextDep)) {
            const n = s.nextDep;
            n.prevDep = s.prevDep, s.prevDep && (s.prevDep.nextDep = n), s.prevDep = q.depsTail, s.nextDep = void 0, q.depsTail.nextDep = s, q.depsTail = s, q.deps === s && (q.deps = n)
        }
        return s
    }

    trigger(t) {
        this.version++, It++, this.notify(t)
    }

    notify(t) {
        qs();
        try {
            for (let s = this.subs; s; s = s.prevSub) s.sub.notify() && s.sub.dep.notify()
        } finally {
            zs()
        }
    }
}

function lr(e) {
    if (e.dep.sc++, e.sub.flags & 4) {
        const t = e.dep.computed;
        if (t && !e.dep.subs) {
            t.flags |= 20;
            for (let n = t.deps; n; n = n.nextDep) lr(n)
        }
        const s = e.dep.subs;
        s !== e && (e.prevSub = s, s && (s.nextSub = e)), e.dep.subs = e
    }
}

const Is = new WeakMap, ot = Symbol(""), Ps = Symbol(""), Pt = Symbol("");

function ce(e, t, s) {
    if (Oe && q) {
        let n = Is.get(e);
        n || Is.set(e, n = new Map);
        let r = n.get(s);
        r || (n.set(s, r = new Ys), r.map = n, r.key = s), r.track()
    }
}

function Ve(e, t, s, n, r, l) {
    const o = Is.get(e);
    if (!o) {
        It++;
        return
    }
    const i = f => {
        f && f.trigger()
    };
    if (qs(), t === "clear") o.forEach(i); else {
        const f = I(e), d = f && Gs(s);
        if (f && s === "length") {
            const a = Number(n);
            o.forEach((h, p) => {
                (p === "length" || p === Pt || !qe(p) && p >= a) && i(h)
            })
        } else switch ((s !== void 0 || o.has(void 0)) && i(o.get(s)), d && i(o.get(Pt)), t) {
            case"add":
                f ? d && i(o.get("length")) : (i(o.get(ot)), dt(e) && i(o.get(Ps)));
                break;
            case"delete":
                f || (i(o.get(ot)), dt(e) && i(o.get(Ps)));
                break;
            case"set":
                dt(e) && i(o.get(ot));
                break
        }
    }
    zs()
}

function ft(e) {
    const t = j(e);
    return t === e ? t : (ce(t, "iterate", Pt), Se(e) ? t : t.map(ie))
}

function us(e) {
    return ce(e = j(e), "iterate", Pt), e
}

const _l = {
    __proto__: null, [Symbol.iterator]() {
        return xs(this, Symbol.iterator, ie)
    }, concat(...e) {
        return ft(this).concat(...e.map(t => I(t) ? ft(t) : t))
    }, entries() {
        return xs(this, "entries", e => (e[1] = ie(e[1]), e))
    }, every(e, t) {
        return He(this, "every", e, t, void 0, arguments)
    }, filter(e, t) {
        return He(this, "filter", e, t, s => s.map(ie), arguments)
    }, find(e, t) {
        return He(this, "find", e, t, ie, arguments)
    }, findIndex(e, t) {
        return He(this, "findIndex", e, t, void 0, arguments)
    }, findLast(e, t) {
        return He(this, "findLast", e, t, ie, arguments)
    }, findLastIndex(e, t) {
        return He(this, "findLastIndex", e, t, void 0, arguments)
    }, forEach(e, t) {
        return He(this, "forEach", e, t, void 0, arguments)
    }, includes(...e) {
        return Ts(this, "includes", e)
    }, indexOf(...e) {
        return Ts(this, "indexOf", e)
    }, join(e) {
        return ft(this).join(e)
    }, lastIndexOf(...e) {
        return Ts(this, "lastIndexOf", e)
    }, map(e, t) {
        return He(this, "map", e, t, void 0, arguments)
    }, pop() {
        return Ct(this, "pop")
    }, push(...e) {
        return Ct(this, "push", e)
    }, reduce(e, ...t) {
        return mn(this, "reduce", e, t)
    }, reduceRight(e, ...t) {
        return mn(this, "reduceRight", e, t)
    }, shift() {
        return Ct(this, "shift")
    }, some(e, t) {
        return He(this, "some", e, t, void 0, arguments)
    }, splice(...e) {
        return Ct(this, "splice", e)
    }, toReversed() {
        return ft(this).toReversed()
    }, toSorted(e) {
        return ft(this).toSorted(e)
    }, toSpliced(...e) {
        return ft(this).toSpliced(...e)
    }, unshift(...e) {
        return Ct(this, "unshift", e)
    }, values() {
        return xs(this, "values", ie)
    }
};

function xs(e, t, s) {
    const n = us(e), r = n[t]();
    return n !== e && !Se(e) && (r._next = r.next, r.next = () => {
        const l = r._next();
        return l.value && (l.value = s(l.value)), l
    }), r
}

const vl = Array.prototype;

function He(e, t, s, n, r, l) {
    const o = us(e), i = o !== e && !Se(e), f = o[t];
    if (f !== vl[t]) {
        const h = f.apply(e, l);
        return i ? ie(h) : h
    }
    let d = s;
    o !== e && (i ? d = function (h, p) {
        return s.call(this, ie(h), p, e)
    } : s.length > 2 && (d = function (h, p) {
        return s.call(this, h, p, e)
    }));
    const a = f.call(o, d, n);
    return i && r ? r(a) : a
}

function mn(e, t, s, n) {
    const r = us(e);
    let l = s;
    return r !== e && (Se(e) ? s.length > 3 && (l = function (o, i, f) {
        return s.call(this, o, i, f, e)
    }) : l = function (o, i, f) {
        return s.call(this, o, ie(i), f, e)
    }), r[t](l, ...n)
}

function Ts(e, t, s) {
    const n = j(e);
    ce(n, "iterate", Pt);
    const r = n[t](...s);
    return (r === -1 || r === !1) && Zs(s[0]) ? (s[0] = j(s[0]), n[t](...s)) : r
}

function Ct(e, t, s = []) {
    Ue(), qs();
    const n = j(e)[t].apply(e, s);
    return zs(), Ge(), n
}

const yl = Ks("__proto__,__v_isRef,__isVue"),
    or = new Set(Object.getOwnPropertyNames(Symbol).filter(e => e !== "arguments" && e !== "caller").map(e => Symbol[e]).filter(qe));

function bl(e) {
    qe(e) || (e = String(e));
    const t = j(this);
    return ce(t, "has", e), t.hasOwnProperty(e)
}

class ir {
    constructor(t = !1, s = !1) {
        this._isReadonly = t, this._isShallow = s
    }

    get(t, s, n) {
        if (s === "__v_skip") return t.__v_skip;
        const r = this._isReadonly, l = this._isShallow;
        if (s === "__v_isReactive") return !r;
        if (s === "__v_isReadonly") return r;
        if (s === "__v_isShallow") return l;
        if (s === "__v_raw") return n === (r ? l ? Rl : ur : l ? ar : fr).get(t) || Object.getPrototypeOf(t) === Object.getPrototypeOf(n) ? t : void 0;
        const o = I(t);
        if (!r) {
            let f;
            if (o && (f = _l[s])) return f;
            if (s === "hasOwnProperty") return bl
        }
        const i = Reflect.get(t, s, ue(t) ? t : n);
        return (qe(s) ? or.has(s) : yl(s)) || (r || ce(t, "get", s), l) ? i : ue(i) ? o && Gs(s) ? i : i.value : X(i) ? r ? dr(i) : kt(i) : i
    }
}

class cr extends ir {
    constructor(t = !1) {
        super(!1, t)
    }

    set(t, s, n, r) {
        let l = t[s];
        if (!this._isShallow) {
            const f = et(l);
            if (!Se(n) && !et(n) && (l = j(l), n = j(n)), !I(t) && ue(l) && !ue(n)) return f ? !1 : (l.value = n, !0)
        }
        const o = I(t) && Gs(s) ? Number(s) < t.length : B(t, s), i = Reflect.set(t, s, n, ue(t) ? t : r);
        return t === j(r) && (o ? Xe(n, l) && Ve(t, "set", s, n) : Ve(t, "add", s, n)), i
    }

    deleteProperty(t, s) {
        const n = B(t, s);
        t[s];
        const r = Reflect.deleteProperty(t, s);
        return r && n && Ve(t, "delete", s, void 0), r
    }

    has(t, s) {
        const n = Reflect.has(t, s);
        return (!qe(s) || !or.has(s)) && ce(t, "has", s), n
    }

    ownKeys(t) {
        return ce(t, "iterate", I(t) ? "length" : ot), Reflect.ownKeys(t)
    }
}

class Cl extends ir {
    constructor(t = !1) {
        super(!0, t)
    }

    set(t, s) {
        return !0
    }

    deleteProperty(t, s) {
        return !0
    }
}

const wl = new cr, xl = new Cl, Tl = new cr(!0);
const Fs = e => e, Gt = e => Reflect.getPrototypeOf(e);

function Sl(e, t, s) {
    return function (...n) {
        const r = this.__v_raw, l = j(r), o = dt(l), i = e === "entries" || e === Symbol.iterator && o,
            f = e === "keys" && o, d = r[e](...n), a = s ? Fs : t ? es : ie;
        return !t && ce(l, "iterate", f ? Ps : ot), {
            next() {
                const {value: h, done: p} = d.next();
                return p ? {value: h, done: p} : {value: i ? [a(h[0]), a(h[1])] : a(h), done: p}
            }, [Symbol.iterator]() {
                return this
            }
        }
    }
}

function Wt(e) {
    return function (...t) {
        return e === "delete" ? !1 : e === "clear" ? void 0 : this
    }
}

function El(e, t) {
    const s = {
        get(r) {
            const l = this.__v_raw, o = j(l), i = j(r);
            e || (Xe(r, i) && ce(o, "get", r), ce(o, "get", i));
            const {has: f} = Gt(o), d = t ? Fs : e ? es : ie;
            if (f.call(o, r)) return d(l.get(r));
            if (f.call(o, i)) return d(l.get(i));
            l !== o && l.get(r)
        }, get size() {
            const r = this.__v_raw;
            return !e && ce(j(r), "iterate", ot), Reflect.get(r, "size", r)
        }, has(r) {
            const l = this.__v_raw, o = j(l), i = j(r);
            return e || (Xe(r, i) && ce(o, "has", r), ce(o, "has", i)), r === i ? l.has(r) : l.has(r) || l.has(i)
        }, forEach(r, l) {
            const o = this, i = o.__v_raw, f = j(i), d = t ? Fs : e ? es : ie;
            return !e && ce(f, "iterate", ot), i.forEach((a, h) => r.call(l, d(a), d(h), o))
        }
    };
    return de(s, e ? {add: Wt("add"), set: Wt("set"), delete: Wt("delete"), clear: Wt("clear")} : {
        add(r) {
            !t && !Se(r) && !et(r) && (r = j(r));
            const l = j(this);
            return Gt(l).has.call(l, r) || (l.add(r), Ve(l, "add", r, r)), this
        }, set(r, l) {
            !t && !Se(l) && !et(l) && (l = j(l));
            const o = j(this), {has: i, get: f} = Gt(o);
            let d = i.call(o, r);
            d || (r = j(r), d = i.call(o, r));
            const a = f.call(o, r);
            return o.set(r, l), d ? Xe(l, a) && Ve(o, "set", r, l) : Ve(o, "add", r, l), this
        }, delete(r) {
            const l = j(this), {has: o, get: i} = Gt(l);
            let f = o.call(l, r);
            f || (r = j(r), f = o.call(l, r)), i && i.call(l, r);
            const d = l.delete(r);
            return f && Ve(l, "delete", r, void 0), d
        }, clear() {
            const r = j(this), l = r.size !== 0, o = r.clear();
            return l && Ve(r, "clear", void 0, void 0), o
        }
    }), ["keys", "values", "entries", Symbol.iterator].forEach(r => {
        s[r] = Sl(r, e, t)
    }), s
}

function Qs(e, t) {
    const s = El(e, t);
    return (n, r, l) => r === "__v_isReactive" ? !e : r === "__v_isReadonly" ? e : r === "__v_raw" ? n : Reflect.get(B(s, r) && r in n ? s : n, r, l)
}

const Al = {get: Qs(!1, !1)}, Ol = {get: Qs(!1, !0)}, Ml = {get: Qs(!0, !1)};
const fr = new WeakMap, ar = new WeakMap, ur = new WeakMap, Rl = new WeakMap;

function $l(e) {
    switch (e) {
        case"Object":
        case"Array":
            return 1;
        case"Map":
        case"Set":
        case"WeakMap":
        case"WeakSet":
            return 2;
        default:
            return 0
    }
}

function Il(e) {
    return e.__v_skip || !Object.isExtensible(e) ? 0 : $l(nl(e))
}

function kt(e) {
    return et(e) ? e : Xs(e, !1, wl, Al, fr)
}

function Pl(e) {
    return Xs(e, !1, Tl, Ol, ar)
}

function dr(e) {
    return Xs(e, !0, xl, Ml, ur)
}

function Xs(e, t, s, n, r) {
    if (!X(e) || e.__v_raw && !(t && e.__v_isReactive)) return e;
    const l = Il(e);
    if (l === 0) return e;
    const o = r.get(e);
    if (o) return o;
    const i = new Proxy(e, l === 2 ? n : s);
    return r.set(e, i), i
}

function ht(e) {
    return et(e) ? ht(e.__v_raw) : !!(e && e.__v_isReactive)
}

function et(e) {
    return !!(e && e.__v_isReadonly)
}

function Se(e) {
    return !!(e && e.__v_isShallow)
}

function Zs(e) {
    return e ? !!e.__v_raw : !1
}

function j(e) {
    const t = e && e.__v_raw;
    return t ? j(t) : e
}

function Fl(e) {
    return !B(e, "__v_skip") && Object.isExtensible(e) && Rs(e, "__v_skip", !0), e
}

const ie = e => X(e) ? kt(e) : e, es = e => X(e) ? dr(e) : e;

function ue(e) {
    return e ? e.__v_isRef === !0 : !1
}

function re(e) {
    return Nl(e, !1)
}

function Nl(e, t) {
    return ue(e) ? e : new Dl(e, t)
}

class Dl {
    constructor(t, s) {
        this.dep = new Ys, this.__v_isRef = !0, this.__v_isShallow = !1, this._rawValue = s ? t : j(t), this._value = s ? t : ie(t), this.__v_isShallow = s
    }

    get value() {
        return this.dep.track(), this._value
    }

    set value(t) {
        const s = this._rawValue, n = this.__v_isShallow || Se(t) || et(t);
        t = n ? t : j(t), Xe(t, s) && (this._rawValue = t, this._value = n ? t : ie(t), this.dep.trigger())
    }
}

function Ae(e) {
    return ue(e) ? e.value : e
}

const Ll = {
    get: (e, t, s) => t === "__v_raw" ? e : Ae(Reflect.get(e, t, s)), set: (e, t, s, n) => {
        const r = e[t];
        return ue(r) && !ue(s) ? (r.value = s, !0) : Reflect.set(e, t, s, n)
    }
};

function hr(e) {
    return ht(e) ? e : new Proxy(e, Ll)
}

class kl {
    constructor(t, s, n) {
        this.fn = t, this.setter = s, this._value = void 0, this.dep = new Ys(this), this.__v_isRef = !0, this.deps = void 0, this.depsTail = void 0, this.flags = 16, this.globalVersion = It - 1, this.next = void 0, this.effect = this, this.__v_isReadonly = !s, this.isSSR = n
    }

    notify() {
        if (this.flags |= 16, !(this.flags & 8) && q !== this) return er(this, !0), !0
    }

    get value() {
        const t = this.dep.track();
        return nr(this), t && (t.version = this.dep.version), this._value
    }

    set value(t) {
        this.setter && this.setter(t)
    }
}

function Hl(e, t, s = !1) {
    let n, r;
    return P(e) ? n = e : (n = e.get, r = e.set), new kl(n, r, s)
}

const qt = {}, ts = new WeakMap;
let lt;

function jl(e, t = !1, s = lt) {
    if (s) {
        let n = ts.get(s);
        n || ts.set(s, n = []), n.push(e)
    }
}

function Bl(e, t, s = z) {
    const {immediate: n, deep: r, once: l, scheduler: o, augmentJob: i, call: f} = s,
        d = w => r ? w : Se(w) || r === !1 || r === 0 ? Qe(w, 1) : Qe(w);
    let a, h, p, _, T = !1, E = !1;
    if (ue(e) ? (h = () => e.value, T = Se(e)) : ht(e) ? (h = () => d(e), T = !0) : I(e) ? (E = !0, T = e.some(w => ht(w) || Se(w)), h = () => e.map(w => {
        if (ue(w)) return w.value;
        if (ht(w)) return d(w);
        if (P(w)) return f ? f(w, 2) : w()
    })) : P(e) ? t ? h = f ? () => f(e, 2) : e : h = () => {
        if (p) {
            Ue();
            try {
                p()
            } finally {
                Ge()
            }
        }
        const w = lt;
        lt = a;
        try {
            return f ? f(e, 3, [_]) : e(_)
        } finally {
            lt = w
        }
    } : h = Le, t && r) {
        const w = h, N = r === !0 ? 1 / 0 : r;
        h = () => Qe(w(), N)
    }
    const k = pl(), R = () => {
        a.stop(), k && k.active && Us(k.effects, a)
    };
    if (l && t) {
        const w = t;
        t = (...N) => {
            w(...N), R()
        }
    }
    let L = E ? new Array(e.length).fill(qt) : qt;
    const U = w => {
        if (!(!(a.flags & 1) || !a.dirty && !w)) if (t) {
            const N = a.run();
            if (r || T || (E ? N.some((J, Y) => Xe(J, L[Y])) : Xe(N, L))) {
                p && p();
                const J = lt;
                lt = a;
                try {
                    const Y = [N, L === qt ? void 0 : E && L[0] === qt ? [] : L, _];
                    L = N, f ? f(t, 3, Y) : t(...Y)
                } finally {
                    lt = J
                }
            }
        } else a.run()
    };
    return i && i(U), a = new Xn(h), a.scheduler = o ? () => o(U, !1) : U, _ = w => jl(w, !1, a), p = a.onStop = () => {
        const w = ts.get(a);
        if (w) {
            if (f) f(w, 4); else for (const N of w) N();
            ts.delete(a)
        }
    }, t ? n ? U(!0) : L = a.run() : o ? o(U.bind(null, !0), !0) : a.run(), R.pause = a.pause.bind(a), R.resume = a.resume.bind(a), R.stop = R, R
}

function Qe(e, t = 1 / 0, s) {
    if (t <= 0 || !X(e) || e.__v_skip || (s = s || new Set, s.has(e))) return e;
    if (s.add(e), t--, ue(e)) Qe(e.value, t, s); else if (I(e)) for (let n = 0; n < e.length; n++) Qe(e[n], t, s); else if (Un(e) || dt(e)) e.forEach(n => {
        Qe(n, t, s)
    }); else if (qn(e)) {
        for (const n in e) Qe(e[n], t, s);
        for (const n of Object.getOwnPropertySymbols(e)) Object.prototype.propertyIsEnumerable.call(e, n) && Qe(e[n], t, s)
    }
    return e
}

/**
 * @vue/runtime-core v3.5.18
 * (c) 2018-present Yuxi (Evan) You and Vue contributors
 * @license MIT
 **/function Ht(e, t, s, n) {
    try {
        return n ? e(...n) : e()
    } catch (r) {
        ds(r, t, s)
    }
}

function ke(e, t, s, n) {
    if (P(e)) {
        const r = Ht(e, t, s, n);
        return r && Gn(r) && r.catch(l => {
            ds(l, t, s)
        }), r
    }
    if (I(e)) {
        const r = [];
        for (let l = 0; l < e.length; l++) r.push(ke(e[l], t, s, n));
        return r
    }
}

function ds(e, t, s, n = !0) {
    const r = t ? t.vnode : null, {errorHandler: l, throwUnhandledErrorInProduction: o} = t && t.appContext.config || z;
    if (t) {
        let i = t.parent;
        const f = t.proxy, d = `https://vuejs.org/error-reference/#runtime-${s}`;
        for (; i;) {
            const a = i.ec;
            if (a) {
                for (let h = 0; h < a.length; h++) if (a[h](e, f, d) === !1) return
            }
            i = i.parent
        }
        if (l) {
            Ue(), Ht(l, null, 10, [e, f, d]), Ge();
            return
        }
    }
    Kl(e, s, r, n, o)
}

function Kl(e, t, s, n = !0, r = !1) {
    if (r) throw e;
    console.error(e)
}

const me = [];
let Ne = -1;
const pt = [];
let Je = null, at = 0;
const pr = Promise.resolve();
let ss = null;

function gr(e) {
    const t = ss || pr;
    return e ? t.then(this ? e.bind(this) : e) : t
}

function Vl(e) {
    let t = Ne + 1, s = me.length;
    for (; t < s;) {
        const n = t + s >>> 1, r = me[n], l = Ft(r);
        l < e || l === e && r.flags & 2 ? t = n + 1 : s = n
    }
    return t
}

function en(e) {
    if (!(e.flags & 1)) {
        const t = Ft(e), s = me[me.length - 1];
        !s || !(e.flags & 2) && t >= Ft(s) ? me.push(e) : me.splice(Vl(t), 0, e), e.flags |= 1, mr()
    }
}

function mr() {
    ss || (ss = pr.then(vr))
}

function Ul(e) {
    I(e) ? pt.push(...e) : Je && e.id === -1 ? Je.splice(at + 1, 0, e) : e.flags & 1 || (pt.push(e), e.flags |= 1), mr()
}

function _n(e, t, s = Ne + 1) {
    for (; s < me.length; s++) {
        const n = me[s];
        if (n && n.flags & 2) {
            if (e && n.id !== e.uid) continue;
            me.splice(s, 1), s--, n.flags & 4 && (n.flags &= -2), n(), n.flags & 4 || (n.flags &= -2)
        }
    }
}

function _r(e) {
    if (pt.length) {
        const t = [...new Set(pt)].sort((s, n) => Ft(s) - Ft(n));
        if (pt.length = 0, Je) {
            Je.push(...t);
            return
        }
        for (Je = t, at = 0; at < Je.length; at++) {
            const s = Je[at];
            s.flags & 4 && (s.flags &= -2), s.flags & 8 || s(), s.flags &= -2
        }
        Je = null, at = 0
    }
}

const Ft = e => e.id == null ? e.flags & 2 ? -1 : 1 / 0 : e.id;

function vr(e) {
    try {
        for (Ne = 0; Ne < me.length; Ne++) {
            const t = me[Ne];
            t && !(t.flags & 8) && (t.flags & 4 && (t.flags &= -2), Ht(t, t.i, t.i ? 15 : 14), t.flags & 4 || (t.flags &= -2))
        }
    } finally {
        for (; Ne < me.length; Ne++) {
            const t = me[Ne];
            t && (t.flags &= -2)
        }
        Ne = -1, me.length = 0, _r(), ss = null, (me.length || pt.length) && vr()
    }
}

let Ce = null, yr = null;

function ns(e) {
    const t = Ce;
    return Ce = e, yr = e && e.type.__scopeId || null, t
}

function Gl(e, t = Ce, s) {
    if (!t || e._n) return e;
    const n = (...r) => {
        n._d && Mn(-1);
        const l = ns(t);
        let o;
        try {
            o = e(...r)
        } finally {
            ns(l), n._d && Mn(1)
        }
        return o
    };
    return n._n = !0, n._c = !0, n._d = !0, n
}

function nt(e, t, s, n) {
    const r = e.dirs, l = t && t.dirs;
    for (let o = 0; o < r.length; o++) {
        const i = r[o];
        l && (i.oldValue = l[o].value);
        let f = i.dir[n];
        f && (Ue(), ke(f, s, 8, [e.el, i, e, t]), Ge())
    }
}

const br = Symbol("_vte"), Wl = e => e.__isTeleport, At = e => e && (e.disabled || e.disabled === ""),
    vn = e => e && (e.defer || e.defer === ""), yn = e => typeof SVGElement < "u" && e instanceof SVGElement,
    bn = e => typeof MathMLElement == "function" && e instanceof MathMLElement, Ns = (e, t) => {
        const s = e && e.to;
        return te(s) ? t ? t(s) : null : s
    }, Cr = {
        name: "Teleport", __isTeleport: !0, process(e, t, s, n, r, l, o, i, f, d) {
            const {mc: a, pc: h, pbc: p, o: {insert: _, querySelector: T, createText: E, createComment: k}} = d,
                R = At(t.props);
            let {shapeFlag: L, children: U, dynamicChildren: w} = t;
            if (e == null) {
                const N = t.el = E(""), J = t.anchor = E("");
                _(N, s, n), _(J, s, n);
                const Y = (G, le) => {
                    L & 16 && (r && r.isCE && (r.ce._teleportTarget = G), a(U, G, le, r, l, o, i, f))
                }, ee = () => {
                    const G = t.target = Ns(t.props, T), le = wr(G, t, E, _);
                    G && (o !== "svg" && yn(G) ? o = "svg" : o !== "mathml" && bn(G) && (o = "mathml"), R || (Y(G, le), Jt(t, !1)))
                };
                R && (Y(s, J), Jt(t, !0)), vn(t.props) ? (t.el.__isMounted = !1, ge(() => {
                    ee(), delete t.el.__isMounted
                }, l)) : ee()
            } else {
                if (vn(t.props) && e.el.__isMounted === !1) {
                    ge(() => {
                        Cr.process(e, t, s, n, r, l, o, i, f, d)
                    }, l);
                    return
                }
                t.el = e.el, t.targetStart = e.targetStart;
                const N = t.anchor = e.anchor, J = t.target = e.target, Y = t.targetAnchor = e.targetAnchor,
                    ee = At(e.props), G = ee ? s : J, le = ee ? N : Y;
                if (o === "svg" || yn(J) ? o = "svg" : (o === "mathml" || bn(J)) && (o = "mathml"), w ? (p(e.dynamicChildren, w, G, r, l, o, i), rn(e, t, !0)) : f || h(e, t, G, le, r, l, o, i, !1), R) ee ? t.props && e.props && t.props.to !== e.props.to && (t.props.to = e.props.to) : zt(t, s, N, d, 1); else if ((t.props && t.props.to) !== (e.props && e.props.to)) {
                    const he = t.target = Ns(t.props, T);
                    he && zt(t, he, null, d, 0)
                } else ee && zt(t, J, Y, d, 1);
                Jt(t, R)
            }
        }, remove(e, t, s, {um: n, o: {remove: r}}, l) {
            const {shapeFlag: o, children: i, anchor: f, targetStart: d, targetAnchor: a, target: h, props: p} = e;
            if (h && (r(d), r(a)), l && r(f), o & 16) {
                const _ = l || !At(p);
                for (let T = 0; T < i.length; T++) {
                    const E = i[T];
                    n(E, t, s, _, !!E.dynamicChildren)
                }
            }
        }, move: zt, hydrate: ql
    };

function zt(e, t, s, {o: {insert: n}, m: r}, l = 2) {
    l === 0 && n(e.targetAnchor, t, s);
    const {el: o, anchor: i, shapeFlag: f, children: d, props: a} = e, h = l === 2;
    if (h && n(o, t, s), (!h || At(a)) && f & 16) for (let p = 0; p < d.length; p++) r(d[p], t, s, 2);
    h && n(i, t, s)
}

function ql(e, t, s, n, r, l, {o: {nextSibling: o, parentNode: i, querySelector: f, insert: d, createText: a}}, h) {
    const p = t.target = Ns(t.props, f);
    if (p) {
        const _ = At(t.props), T = p._lpa || p.firstChild;
        if (t.shapeFlag & 16) if (_) t.anchor = h(o(e), t, i(e), s, n, r, l), t.targetStart = T, t.targetAnchor = T && o(T); else {
            t.anchor = o(e);
            let E = T;
            for (; E;) {
                if (E && E.nodeType === 8) {
                    if (E.data === "teleport start anchor") t.targetStart = E; else if (E.data === "teleport anchor") {
                        t.targetAnchor = E, p._lpa = t.targetAnchor && o(t.targetAnchor);
                        break
                    }
                }
                E = o(E)
            }
            t.targetAnchor || wr(p, t, a, d), h(T && o(T), t, p, s, n, r, l)
        }
        Jt(t, _)
    }
    return t.anchor && o(t.anchor)
}

const zl = Cr;

function Jt(e, t) {
    const s = e.ctx;
    if (s && s.ut) {
        let n, r;
        for (t ? (n = e.el, r = e.anchor) : (n = e.targetStart, r = e.targetAnchor); n && n !== r;) n.nodeType === 1 && n.setAttribute("data-v-owner", s.uid), n = n.nextSibling;
        s.ut()
    }
}

function wr(e, t, s, n) {
    const r = t.targetStart = s(""), l = t.targetAnchor = s("");
    return r[br] = l, e && (n(r, e), n(l, e)), l
}

function tn(e, t) {
    e.shapeFlag & 6 && e.component ? (e.transition = t, tn(e.component.subTree, t)) : e.shapeFlag & 128 ? (e.ssContent.transition = t.clone(e.ssContent), e.ssFallback.transition = t.clone(e.ssFallback)) : e.transition = t
}/*! #__NO_SIDE_EFFECTS__ */
function jt(e, t) {
    return P(e) ? de({name: e.name}, t, {setup: e}) : e
}

function xr(e) {
    e.ids = [e.ids[0] + e.ids[2]++ + "-", 0, 0]
}

function Ot(e, t, s, n, r = !1) {
    if (I(e)) {
        e.forEach((T, E) => Ot(T, t && (I(t) ? t[E] : t), s, n, r));
        return
    }
    if (gt(n) && !r) {
        n.shapeFlag & 512 && n.type.__asyncResolved && n.component.subTree.component && Ot(e, t, s, n.component.subTree);
        return
    }
    const l = n.shapeFlag & 4 ? cn(n.component) : n.el, o = r ? null : l, {i, r: f} = e, d = t && t.r,
        a = i.refs === z ? i.refs = {} : i.refs, h = i.setupState, p = j(h), _ = h === z ? () => !1 : T => B(p, T);
    if (d != null && d !== f && (te(d) ? (a[d] = null, _(d) && (h[d] = null)) : ue(d) && (d.value = null)), P(f)) Ht(f, i, 12, [o, a]); else {
        const T = te(f), E = ue(f);
        if (T || E) {
            const k = () => {
                if (e.f) {
                    const R = T ? _(f) ? h[f] : a[f] : f.value;
                    r ? I(R) && Us(R, l) : I(R) ? R.includes(l) || R.push(l) : T ? (a[f] = [l], _(f) && (h[f] = a[f])) : (f.value = [l], e.k && (a[e.k] = f.value))
                } else T ? (a[f] = o, _(f) && (h[f] = o)) : E && (f.value = o, e.k && (a[e.k] = o))
            };
            o ? (k.id = -1, ge(k, s)) : k()
        }
    }
}

fs().requestIdleCallback;
fs().cancelIdleCallback;
const gt = e => !!e.type.__asyncLoader, Tr = e => e.type.__isKeepAlive;

function Jl(e, t) {
    Sr(e, "a", t)
}

function Yl(e, t) {
    Sr(e, "da", t)
}

function Sr(e, t, s = _e) {
    const n = e.__wdc || (e.__wdc = () => {
        let r = s;
        for (; r;) {
            if (r.isDeactivated) return;
            r = r.parent
        }
        return e()
    });
    if (hs(t, n, s), s) {
        let r = s.parent;
        for (; r && r.parent;) Tr(r.parent.vnode) && Ql(n, t, s, r), r = r.parent
    }
}

function Ql(e, t, s, n) {
    const r = hs(t, e, n, !0);
    gs(() => {
        Us(n[t], r)
    }, s)
}

function hs(e, t, s = _e, n = !1) {
    if (s) {
        const r = s[e] || (s[e] = []), l = t.__weh || (t.__weh = (...o) => {
            Ue();
            const i = Bt(s), f = ke(t, s, e, o);
            return i(), Ge(), f
        });
        return n ? r.unshift(l) : r.push(l), l
    }
}

const ze = e => (t, s = _e) => {
        (!Lt || e === "sp") && hs(e, (...n) => t(...n), s)
    }, Xl = ze("bm"), ps = ze("m"), Zl = ze("bu"), eo = ze("u"), to = ze("bum"), gs = ze("um"), so = ze("sp"),
    no = ze("rtg"), ro = ze("rtc");

function lo(e, t = _e) {
    hs("ec", e, t)
}

const oo = Symbol.for("v-ndc");

function Yt(e, t, s, n) {
    let r;
    const l = s, o = I(e);
    if (o || te(e)) {
        const i = o && ht(e);
        let f = !1, d = !1;
        i && (f = !Se(e), d = et(e), e = us(e)), r = new Array(e.length);
        for (let a = 0, h = e.length; a < h; a++) r[a] = t(f ? d ? es(ie(e[a])) : ie(e[a]) : e[a], a, void 0, l)
    } else if (typeof e == "number") {
        r = new Array(e);
        for (let i = 0; i < e; i++) r[i] = t(i + 1, i, void 0, l)
    } else if (X(e)) if (e[Symbol.iterator]) r = Array.from(e, (i, f) => t(i, f, void 0, l)); else {
        const i = Object.keys(e);
        r = new Array(i.length);
        for (let f = 0, d = i.length; f < d; f++) {
            const a = i[f];
            r[f] = t(e[a], a, f, l)
        }
    } else r = [];
    return r
}

function io(e, t, s = {}, n, r) {
    if (Ce.ce || Ce.parent && gt(Ce.parent) && Ce.parent.ce) return Q(), it(fe, null, [Me("slot", s, n && n())], 64);
    let l = e[t];
    l && l._c && (l._d = !1), Q();
    const o = l && Er(l(s)), i = s.key || o && o.key,
        f = it(fe, {key: (i && !qe(i) ? i : `_${t}`) + (!o && n ? "_fb" : "")}, o || (n ? n() : []), o && e._ === 1 ? 64 : -2);
    return l && l._c && (l._d = !0), f
}

function Er(e) {
    return e.some(t => ln(t) ? !(t.type === We || t.type === fe && !Er(t.children)) : !0) ? e : null
}

const Ds = e => e ? Gr(e) ? cn(e) : Ds(e.parent) : null, Mt = de(Object.create(null), {
    $: e => e,
    $el: e => e.vnode.el,
    $data: e => e.data,
    $props: e => e.props,
    $attrs: e => e.attrs,
    $slots: e => e.slots,
    $refs: e => e.refs,
    $parent: e => Ds(e.parent),
    $root: e => Ds(e.root),
    $host: e => e.ce,
    $emit: e => e.emit,
    $options: e => Or(e),
    $forceUpdate: e => e.f || (e.f = () => {
        en(e.update)
    }),
    $nextTick: e => e.n || (e.n = gr.bind(e.proxy)),
    $watch: e => Ro.bind(e)
}), Ss = (e, t) => e !== z && !e.__isScriptSetup && B(e, t), co = {
    get({_: e}, t) {
        if (t === "__v_skip") return !0;
        const {ctx: s, setupState: n, data: r, props: l, accessCache: o, type: i, appContext: f} = e;
        let d;
        if (t[0] !== "$") {
            const _ = o[t];
            if (_ !== void 0) switch (_) {
                case 1:
                    return n[t];
                case 2:
                    return r[t];
                case 4:
                    return s[t];
                case 3:
                    return l[t]
            } else {
                if (Ss(n, t)) return o[t] = 1, n[t];
                if (r !== z && B(r, t)) return o[t] = 2, r[t];
                if ((d = e.propsOptions[0]) && B(d, t)) return o[t] = 3, l[t];
                if (s !== z && B(s, t)) return o[t] = 4, s[t];
                Ls && (o[t] = 0)
            }
        }
        const a = Mt[t];
        let h, p;
        if (a) return t === "$attrs" && ce(e.attrs, "get", ""), a(e);
        if ((h = i.__cssModules) && (h = h[t])) return h;
        if (s !== z && B(s, t)) return o[t] = 4, s[t];
        if (p = f.config.globalProperties, B(p, t)) return p[t]
    }, set({_: e}, t, s) {
        const {data: n, setupState: r, ctx: l} = e;
        return Ss(r, t) ? (r[t] = s, !0) : n !== z && B(n, t) ? (n[t] = s, !0) : B(e.props, t) || t[0] === "$" && t.slice(1) in e ? !1 : (l[t] = s, !0)
    }, has({_: {data: e, setupState: t, accessCache: s, ctx: n, appContext: r, propsOptions: l}}, o) {
        let i;
        return !!s[o] || e !== z && B(e, o) || Ss(t, o) || (i = l[0]) && B(i, o) || B(n, o) || B(Mt, o) || B(r.config.globalProperties, o)
    }, defineProperty(e, t, s) {
        return s.get != null ? e._.accessCache[t] = 0 : B(s, "value") && this.set(e, t, s.value, null), Reflect.defineProperty(e, t, s)
    }
};

function Cn(e) {
    return I(e) ? e.reduce((t, s) => (t[s] = null, t), {}) : e
}

let Ls = !0;

function fo(e) {
    const t = Or(e), s = e.proxy, n = e.ctx;
    Ls = !1, t.beforeCreate && wn(t.beforeCreate, e, "bc");
    const {
        data: r,
        computed: l,
        methods: o,
        watch: i,
        provide: f,
        inject: d,
        created: a,
        beforeMount: h,
        mounted: p,
        beforeUpdate: _,
        updated: T,
        activated: E,
        deactivated: k,
        beforeDestroy: R,
        beforeUnmount: L,
        destroyed: U,
        unmounted: w,
        render: N,
        renderTracked: J,
        renderTriggered: Y,
        errorCaptured: ee,
        serverPrefetch: G,
        expose: le,
        inheritAttrs: he,
        components: Ee,
        directives: Z,
        filters: se
    } = t;
    if (d && ao(d, n, null), o) for (const H in o) {
        const V = o[H];
        P(V) && (n[H] = V.bind(s))
    }
    if (r) {
        const H = r.call(s, s);
        X(H) && (e.data = kt(H))
    }
    if (Ls = !0, l) for (const H in l) {
        const V = l[H], tt = P(V) ? V.bind(s, s) : P(V.get) ? V.get.bind(s, s) : Le,
            Vt = !P(V) && P(V.set) ? V.set.bind(s) : Le, st = Ke({get: tt, set: Vt});
        Object.defineProperty(n, H, {enumerable: !0, configurable: !0, get: () => st.value, set: Re => st.value = Re})
    }
    if (i) for (const H in i) Ar(i[H], n, s, H);
    if (f) {
        const H = P(f) ? f.call(s) : f;
        Reflect.ownKeys(H).forEach(V => {
            _o(V, H[V])
        })
    }
    a && wn(a, e, "c");

    function ne(H, V) {
        I(V) ? V.forEach(tt => H(tt.bind(s))) : V && H(V.bind(s))
    }

    if (ne(Xl, h), ne(ps, p), ne(Zl, _), ne(eo, T), ne(Jl, E), ne(Yl, k), ne(lo, ee), ne(ro, J), ne(no, Y), ne(to, L), ne(gs, w), ne(so, G), I(le)) if (le.length) {
        const H = e.exposed || (e.exposed = {});
        le.forEach(V => {
            Object.defineProperty(H, V, {get: () => s[V], set: tt => s[V] = tt, enumerable: !0})
        })
    } else e.exposed || (e.exposed = {});
    N && e.render === Le && (e.render = N), he != null && (e.inheritAttrs = he), Ee && (e.components = Ee), Z && (e.directives = Z), G && xr(e)
}

function ao(e, t, s = Le) {
    I(e) && (e = ks(e));
    for (const n in e) {
        const r = e[n];
        let l;
        X(r) ? "default" in r ? l = Qt(r.from || n, r.default, !0) : l = Qt(r.from || n) : l = Qt(r), ue(l) ? Object.defineProperty(t, n, {
            enumerable: !0,
            configurable: !0,
            get: () => l.value,
            set: o => l.value = o
        }) : t[n] = l
    }
}

function wn(e, t, s) {
    ke(I(e) ? e.map(n => n.bind(t.proxy)) : e.bind(t.proxy), t, s)
}

function Ar(e, t, s, n) {
    let r = n.includes(".") ? jr(s, n) : () => s[n];
    if (te(e)) {
        const l = t[e];
        P(l) && Rt(r, l)
    } else if (P(e)) Rt(r, e.bind(s)); else if (X(e)) if (I(e)) e.forEach(l => Ar(l, t, s, n)); else {
        const l = P(e.handler) ? e.handler.bind(s) : t[e.handler];
        P(l) && Rt(r, l, e)
    }
}

function Or(e) {
    const t = e.type, {mixins: s, extends: n} = t, {
        mixins: r,
        optionsCache: l,
        config: {optionMergeStrategies: o}
    } = e.appContext, i = l.get(t);
    let f;
    return i ? f = i : !r.length && !s && !n ? f = t : (f = {}, r.length && r.forEach(d => rs(f, d, o, !0)), rs(f, t, o)), X(t) && l.set(t, f), f
}

function rs(e, t, s, n = !1) {
    const {mixins: r, extends: l} = t;
    l && rs(e, l, s, !0), r && r.forEach(o => rs(e, o, s, !0));
    for (const o in t) if (!(n && o === "expose")) {
        const i = uo[o] || s && s[o];
        e[o] = i ? i(e[o], t[o]) : t[o]
    }
    return e
}

const uo = {
    data: xn,
    props: Tn,
    emits: Tn,
    methods: xt,
    computed: xt,
    beforeCreate: pe,
    created: pe,
    beforeMount: pe,
    mounted: pe,
    beforeUpdate: pe,
    updated: pe,
    beforeDestroy: pe,
    beforeUnmount: pe,
    destroyed: pe,
    unmounted: pe,
    activated: pe,
    deactivated: pe,
    errorCaptured: pe,
    serverPrefetch: pe,
    components: xt,
    directives: xt,
    watch: po,
    provide: xn,
    inject: ho
};

function xn(e, t) {
    return t ? e ? function () {
        return de(P(e) ? e.call(this, this) : e, P(t) ? t.call(this, this) : t)
    } : t : e
}

function ho(e, t) {
    return xt(ks(e), ks(t))
}

function ks(e) {
    if (I(e)) {
        const t = {};
        for (let s = 0; s < e.length; s++) t[e[s]] = e[s];
        return t
    }
    return e
}

function pe(e, t) {
    return e ? [...new Set([].concat(e, t))] : t
}

function xt(e, t) {
    return e ? de(Object.create(null), e, t) : t
}

function Tn(e, t) {
    return e ? I(e) && I(t) ? [...new Set([...e, ...t])] : de(Object.create(null), Cn(e), Cn(t ?? {})) : t
}

function po(e, t) {
    if (!e) return t;
    if (!t) return e;
    const s = de(Object.create(null), e);
    for (const n in t) s[n] = pe(e[n], t[n]);
    return s
}

function Mr() {
    return {
        app: null,
        config: {
            isNativeTag: tl,
            performance: !1,
            globalProperties: {},
            optionMergeStrategies: {},
            errorHandler: void 0,
            warnHandler: void 0,
            compilerOptions: {}
        },
        mixins: [],
        components: {},
        directives: {},
        provides: Object.create(null),
        optionsCache: new WeakMap,
        propsCache: new WeakMap,
        emitsCache: new WeakMap
    }
}

let go = 0;

function mo(e, t) {
    return function (n, r = null) {
        P(n) || (n = de({}, n)), r != null && !X(r) && (r = null);
        const l = Mr(), o = new WeakSet, i = [];
        let f = !1;
        const d = l.app = {
            _uid: go++,
            _component: n,
            _props: r,
            _container: null,
            _context: l,
            _instance: null,
            version: Qo,
            get config() {
                return l.config
            },
            set config(a) {
            },
            use(a, ...h) {
                return o.has(a) || (a && P(a.install) ? (o.add(a), a.install(d, ...h)) : P(a) && (o.add(a), a(d, ...h))), d
            },
            mixin(a) {
                return l.mixins.includes(a) || l.mixins.push(a), d
            },
            component(a, h) {
                return h ? (l.components[a] = h, d) : l.components[a]
            },
            directive(a, h) {
                return h ? (l.directives[a] = h, d) : l.directives[a]
            },
            mount(a, h, p) {
                if (!f) {
                    const _ = d._ceVNode || Me(n, r);
                    return _.appContext = l, p === !0 ? p = "svg" : p === !1 && (p = void 0), e(_, a, p), f = !0, d._container = a, a.__vue_app__ = d, cn(_.component)
                }
            },
            onUnmount(a) {
                i.push(a)
            },
            unmount() {
                f && (ke(i, d._instance, 16), e(null, d._container), delete d._container.__vue_app__)
            },
            provide(a, h) {
                return l.provides[a] = h, d
            },
            runWithContext(a) {
                const h = mt;
                mt = d;
                try {
                    return a()
                } finally {
                    mt = h
                }
            }
        };
        return d
    }
}

let mt = null;

function _o(e, t) {
    if (_e) {
        let s = _e.provides;
        const n = _e.parent && _e.parent.provides;
        n === s && (s = _e.provides = Object.create(n)), s[e] = t
    }
}

function Qt(e, t, s = !1) {
    const n = Go();
    if (n || mt) {
        let r = mt ? mt._context.provides : n ? n.parent == null || n.ce ? n.vnode.appContext && n.vnode.appContext.provides : n.parent.provides : void 0;
        if (r && e in r) return r[e];
        if (arguments.length > 1) return s && P(t) ? t.call(n && n.proxy) : t
    }
}

const Rr = {}, $r = () => Object.create(Rr), Ir = e => Object.getPrototypeOf(e) === Rr;

function vo(e, t, s, n = !1) {
    const r = {}, l = $r();
    e.propsDefaults = Object.create(null), Pr(e, t, r, l);
    for (const o in e.propsOptions[0]) o in r || (r[o] = void 0);
    s ? e.props = n ? r : Pl(r) : e.type.props ? e.props = r : e.props = l, e.attrs = l
}

function yo(e, t, s, n) {
    const {props: r, attrs: l, vnode: {patchFlag: o}} = e, i = j(r), [f] = e.propsOptions;
    let d = !1;
    if ((n || o > 0) && !(o & 16)) {
        if (o & 8) {
            const a = e.vnode.dynamicProps;
            for (let h = 0; h < a.length; h++) {
                let p = a[h];
                if (ms(e.emitsOptions, p)) continue;
                const _ = t[p];
                if (f) if (B(l, p)) _ !== l[p] && (l[p] = _, d = !0); else {
                    const T = Ze(p);
                    r[T] = Hs(f, i, T, _, e, !1)
                } else _ !== l[p] && (l[p] = _, d = !0)
            }
        }
    } else {
        Pr(e, t, r, l) && (d = !0);
        let a;
        for (const h in i) (!t || !B(t, h) && ((a = ct(h)) === h || !B(t, a))) && (f ? s && (s[h] !== void 0 || s[a] !== void 0) && (r[h] = Hs(f, i, h, void 0, e, !0)) : delete r[h]);
        if (l !== i) for (const h in l) (!t || !B(t, h)) && (delete l[h], d = !0)
    }
    d && Ve(e.attrs, "set", "")
}

function Pr(e, t, s, n) {
    const [r, l] = e.propsOptions;
    let o = !1, i;
    if (t) for (let f in t) {
        if (Tt(f)) continue;
        const d = t[f];
        let a;
        r && B(r, a = Ze(f)) ? !l || !l.includes(a) ? s[a] = d : (i || (i = {}))[a] = d : ms(e.emitsOptions, f) || (!(f in n) || d !== n[f]) && (n[f] = d, o = !0)
    }
    if (l) {
        const f = j(s), d = i || z;
        for (let a = 0; a < l.length; a++) {
            const h = l[a];
            s[h] = Hs(r, f, h, d[h], e, !B(d, h))
        }
    }
    return o
}

function Hs(e, t, s, n, r, l) {
    const o = e[s];
    if (o != null) {
        const i = B(o, "default");
        if (i && n === void 0) {
            const f = o.default;
            if (o.type !== Function && !o.skipFactory && P(f)) {
                const {propsDefaults: d} = r;
                if (s in d) n = d[s]; else {
                    const a = Bt(r);
                    n = d[s] = f.call(null, t), a()
                }
            } else n = f;
            r.ce && r.ce._setProp(s, n)
        }
        o[0] && (l && !i ? n = !1 : o[1] && (n === "" || n === ct(s)) && (n = !0))
    }
    return n
}

const bo = new WeakMap;

function Fr(e, t, s = !1) {
    const n = s ? bo : t.propsCache, r = n.get(e);
    if (r) return r;
    const l = e.props, o = {}, i = [];
    let f = !1;
    if (!P(e)) {
        const a = h => {
            f = !0;
            const [p, _] = Fr(h, t, !0);
            de(o, p), _ && i.push(..._)
        };
        !s && t.mixins.length && t.mixins.forEach(a), e.extends && a(e.extends), e.mixins && e.mixins.forEach(a)
    }
    if (!l && !f) return X(e) && n.set(e, ut), ut;
    if (I(l)) for (let a = 0; a < l.length; a++) {
        const h = Ze(l[a]);
        Sn(h) && (o[h] = z)
    } else if (l) for (const a in l) {
        const h = Ze(a);
        if (Sn(h)) {
            const p = l[a], _ = o[h] = I(p) || P(p) ? {type: p} : de({}, p), T = _.type;
            let E = !1, k = !0;
            if (I(T)) for (let R = 0; R < T.length; ++R) {
                const L = T[R], U = P(L) && L.name;
                if (U === "Boolean") {
                    E = !0;
                    break
                } else U === "String" && (k = !1)
            } else E = P(T) && T.name === "Boolean";
            _[0] = E, _[1] = k, (E || B(_, "default")) && i.push(h)
        }
    }
    const d = [o, i];
    return X(e) && n.set(e, d), d
}

function Sn(e) {
    return e[0] !== "$" && !Tt(e)
}

const sn = e => e === "_" || e === "__" || e === "_ctx" || e === "$stable", nn = e => I(e) ? e.map(De) : [De(e)],
    Co = (e, t, s) => {
        if (t._n) return t;
        const n = Gl((...r) => nn(t(...r)), s);
        return n._c = !1, n
    }, Nr = (e, t, s) => {
        const n = e._ctx;
        for (const r in e) {
            if (sn(r)) continue;
            const l = e[r];
            if (P(l)) t[r] = Co(r, l, n); else if (l != null) {
                const o = nn(l);
                t[r] = () => o
            }
        }
    }, Dr = (e, t) => {
        const s = nn(t);
        e.slots.default = () => s
    }, Lr = (e, t, s) => {
        for (const n in t) (s || !sn(n)) && (e[n] = t[n])
    }, wo = (e, t, s) => {
        const n = e.slots = $r();
        if (e.vnode.shapeFlag & 32) {
            const r = t.__;
            r && Rs(n, "__", r, !0);
            const l = t._;
            l ? (Lr(n, t, s), s && Rs(n, "_", l, !0)) : Nr(t, n)
        } else t && Dr(e, t)
    }, xo = (e, t, s) => {
        const {vnode: n, slots: r} = e;
        let l = !0, o = z;
        if (n.shapeFlag & 32) {
            const i = t._;
            i ? s && i === 1 ? l = !1 : Lr(r, t, s) : (l = !t.$stable, Nr(t, r)), o = t
        } else t && (Dr(e, t), o = {default: 1});
        if (l) for (const i in r) !sn(i) && o[i] == null && delete r[i]
    }, ge = Lo;

function To(e) {
    return So(e)
}

function So(e, t) {
    const s = fs();
    s.__VUE__ = !0;
    const {
        insert: n,
        remove: r,
        patchProp: l,
        createElement: o,
        createText: i,
        createComment: f,
        setText: d,
        setElementText: a,
        parentNode: h,
        nextSibling: p,
        setScopeId: _ = Le,
        insertStaticContent: T
    } = e, E = (c, u, g, y = null, m = null, v = null, S = void 0, x = null, C = !!u.dynamicChildren) => {
        if (c === u) return;
        c && !wt(c, u) && (y = Ut(c), Re(c, m, v, !0), c = null), u.patchFlag === -2 && (C = !1, u.dynamicChildren = null);
        const {type: b, ref: M, shapeFlag: A} = u;
        switch (b) {
            case _s:
                k(c, u, g, y);
                break;
            case We:
                R(c, u, g, y);
                break;
            case As:
                c == null && L(u, g, y, S);
                break;
            case fe:
                Ee(c, u, g, y, m, v, S, x, C);
                break;
            default:
                A & 1 ? N(c, u, g, y, m, v, S, x, C) : A & 6 ? Z(c, u, g, y, m, v, S, x, C) : (A & 64 || A & 128) && b.process(c, u, g, y, m, v, S, x, C, yt)
        }
        M != null && m ? Ot(M, c && c.ref, v, u || c, !u) : M == null && c && c.ref != null && Ot(c.ref, null, v, c, !0)
    }, k = (c, u, g, y) => {
        if (c == null) n(u.el = i(u.children), g, y); else {
            const m = u.el = c.el;
            u.children !== c.children && d(m, u.children)
        }
    }, R = (c, u, g, y) => {
        c == null ? n(u.el = f(u.children || ""), g, y) : u.el = c.el
    }, L = (c, u, g, y) => {
        [c.el, c.anchor] = T(c.children, u, g, y, c.el, c.anchor)
    }, U = ({el: c, anchor: u}, g, y) => {
        let m;
        for (; c && c !== u;) m = p(c), n(c, g, y), c = m;
        n(u, g, y)
    }, w = ({el: c, anchor: u}) => {
        let g;
        for (; c && c !== u;) g = p(c), r(c), c = g;
        r(u)
    }, N = (c, u, g, y, m, v, S, x, C) => {
        u.type === "svg" ? S = "svg" : u.type === "math" && (S = "mathml"), c == null ? J(u, g, y, m, v, S, x, C) : G(c, u, m, v, S, x, C)
    }, J = (c, u, g, y, m, v, S, x) => {
        let C, b;
        const {props: M, shapeFlag: A, transition: O, dirs: $} = c;
        if (C = c.el = o(c.type, v, M && M.is, M), A & 8 ? a(C, c.children) : A & 16 && ee(c.children, C, null, y, m, Es(c, v), S, x), $ && nt(c, null, y, "created"), Y(C, c, c.scopeId, S, y), M) {
            for (const W in M) W !== "value" && !Tt(W) && l(C, W, null, M[W], v, y);
            "value" in M && l(C, "value", null, M.value, v), (b = M.onVnodeBeforeMount) && Fe(b, y, c)
        }
        $ && nt(c, null, y, "beforeMount");
        const D = Eo(m, O);
        D && O.beforeEnter(C), n(C, u, g), ((b = M && M.onVnodeMounted) || D || $) && ge(() => {
            b && Fe(b, y, c), D && O.enter(C), $ && nt(c, null, y, "mounted")
        }, m)
    }, Y = (c, u, g, y, m) => {
        if (g && _(c, g), y) for (let v = 0; v < y.length; v++) _(c, y[v]);
        if (m) {
            let v = m.subTree;
            if (u === v || Kr(v.type) && (v.ssContent === u || v.ssFallback === u)) {
                const S = m.vnode;
                Y(c, S, S.scopeId, S.slotScopeIds, m.parent)
            }
        }
    }, ee = (c, u, g, y, m, v, S, x, C = 0) => {
        for (let b = C; b < c.length; b++) {
            const M = c[b] = x ? Ye(c[b]) : De(c[b]);
            E(null, M, u, g, y, m, v, S, x)
        }
    }, G = (c, u, g, y, m, v, S) => {
        const x = u.el = c.el;
        let {patchFlag: C, dynamicChildren: b, dirs: M} = u;
        C |= c.patchFlag & 16;
        const A = c.props || z, O = u.props || z;
        let $;
        if (g && rt(g, !1), ($ = O.onVnodeBeforeUpdate) && Fe($, g, u, c), M && nt(u, c, g, "beforeUpdate"), g && rt(g, !0), (A.innerHTML && O.innerHTML == null || A.textContent && O.textContent == null) && a(x, ""), b ? le(c.dynamicChildren, b, x, g, y, Es(u, m), v) : S || V(c, u, x, null, g, y, Es(u, m), v, !1), C > 0) {
            if (C & 16) he(x, A, O, g, m); else if (C & 2 && A.class !== O.class && l(x, "class", null, O.class, m), C & 4 && l(x, "style", A.style, O.style, m), C & 8) {
                const D = u.dynamicProps;
                for (let W = 0; W < D.length; W++) {
                    const K = D[W], ve = A[K], ye = O[K];
                    (ye !== ve || K === "value") && l(x, K, ve, ye, m, g)
                }
            }
            C & 1 && c.children !== u.children && a(x, u.children)
        } else !S && b == null && he(x, A, O, g, m);
        (($ = O.onVnodeUpdated) || M) && ge(() => {
            $ && Fe($, g, u, c), M && nt(u, c, g, "updated")
        }, y)
    }, le = (c, u, g, y, m, v, S) => {
        for (let x = 0; x < u.length; x++) {
            const C = c[x], b = u[x], M = C.el && (C.type === fe || !wt(C, b) || C.shapeFlag & 198) ? h(C.el) : g;
            E(C, b, M, null, y, m, v, S, !0)
        }
    }, he = (c, u, g, y, m) => {
        if (u !== g) {
            if (u !== z) for (const v in u) !Tt(v) && !(v in g) && l(c, v, u[v], null, m, y);
            for (const v in g) {
                if (Tt(v)) continue;
                const S = g[v], x = u[v];
                S !== x && v !== "value" && l(c, v, x, S, m, y)
            }
            "value" in g && l(c, "value", u.value, g.value, m)
        }
    }, Ee = (c, u, g, y, m, v, S, x, C) => {
        const b = u.el = c ? c.el : i(""), M = u.anchor = c ? c.anchor : i("");
        let {patchFlag: A, dynamicChildren: O, slotScopeIds: $} = u;
        $ && (x = x ? x.concat($) : $), c == null ? (n(b, g, y), n(M, g, y), ee(u.children || [], g, M, m, v, S, x, C)) : A > 0 && A & 64 && O && c.dynamicChildren ? (le(c.dynamicChildren, O, g, m, v, S, x), (u.key != null || m && u === m.subTree) && rn(c, u, !0)) : V(c, u, g, M, m, v, S, x, C)
    }, Z = (c, u, g, y, m, v, S, x, C) => {
        u.slotScopeIds = x, c == null ? u.shapeFlag & 512 ? m.ctx.activate(u, g, y, S, C) : se(u, g, y, m, v, S, C) : oe(c, u, C)
    }, se = (c, u, g, y, m, v, S) => {
        const x = c.component = Uo(c, y, m);
        if (Tr(c) && (x.ctx.renderer = yt), Wo(x, !1, S), x.asyncDep) {
            if (m && m.registerDep(x, ne, S), !c.el) {
                const C = x.subTree = Me(We);
                R(null, C, u, g), c.placeholder = C.el
            }
        } else ne(x, c, u, g, m, v, S)
    }, oe = (c, u, g) => {
        const y = u.component = c.component;
        if (No(c, u, g)) if (y.asyncDep && !y.asyncResolved) {
            H(y, u, g);
            return
        } else y.next = u, y.update(); else u.el = c.el, y.vnode = u
    }, ne = (c, u, g, y, m, v, S) => {
        const x = () => {
            if (c.isMounted) {
                let {next: A, bu: O, u: $, parent: D, vnode: W} = c;
                {
                    const Ie = kr(c);
                    if (Ie) {
                        A && (A.el = W.el, H(c, A, S)), Ie.asyncDep.then(() => {
                            c.isUnmounted || x()
                        });
                        return
                    }
                }
                let K = A, ve;
                rt(c, !1), A ? (A.el = W.el, H(c, A, S)) : A = W, O && bs(O), (ve = A.props && A.props.onVnodeBeforeUpdate) && Fe(ve, D, A, W), rt(c, !0);
                const ye = An(c), $e = c.subTree;
                c.subTree = ye, E($e, ye, h($e.el), Ut($e), c, m, v), A.el = ye.el, K === null && Do(c, ye.el), $ && ge($, m), (ve = A.props && A.props.onVnodeUpdated) && ge(() => Fe(ve, D, A, W), m)
            } else {
                let A;
                const {el: O, props: $} = u, {bm: D, m: W, parent: K, root: ve, type: ye} = c, $e = gt(u);
                rt(c, !1), D && bs(D), !$e && (A = $ && $.onVnodeBeforeMount) && Fe(A, K, u), rt(c, !0);
                {
                    ve.ce && ve.ce._def.shadowRoot !== !1 && ve.ce._injectChildStyle(ye);
                    const Ie = c.subTree = An(c);
                    E(null, Ie, g, y, c, m, v), u.el = Ie.el
                }
                if (W && ge(W, m), !$e && (A = $ && $.onVnodeMounted)) {
                    const Ie = u;
                    ge(() => Fe(A, K, Ie), m)
                }
                (u.shapeFlag & 256 || K && gt(K.vnode) && K.vnode.shapeFlag & 256) && c.a && ge(c.a, m), c.isMounted = !0, u = g = y = null
            }
        };
        c.scope.on();
        const C = c.effect = new Xn(x);
        c.scope.off();
        const b = c.update = C.run.bind(C), M = c.job = C.runIfDirty.bind(C);
        M.i = c, M.id = c.uid, C.scheduler = () => en(M), rt(c, !0), b()
    }, H = (c, u, g) => {
        u.component = c;
        const y = c.vnode.props;
        c.vnode = u, c.next = null, yo(c, u.props, y, g), xo(c, u.children, g), Ue(), _n(c), Ge()
    }, V = (c, u, g, y, m, v, S, x, C = !1) => {
        const b = c && c.children, M = c ? c.shapeFlag : 0, A = u.children, {patchFlag: O, shapeFlag: $} = u;
        if (O > 0) {
            if (O & 128) {
                Vt(b, A, g, y, m, v, S, x, C);
                return
            } else if (O & 256) {
                tt(b, A, g, y, m, v, S, x, C);
                return
            }
        }
        $ & 8 ? (M & 16 && vt(b, m, v), A !== b && a(g, A)) : M & 16 ? $ & 16 ? Vt(b, A, g, y, m, v, S, x, C) : vt(b, m, v, !0) : (M & 8 && a(g, ""), $ & 16 && ee(A, g, y, m, v, S, x, C))
    }, tt = (c, u, g, y, m, v, S, x, C) => {
        c = c || ut, u = u || ut;
        const b = c.length, M = u.length, A = Math.min(b, M);
        let O;
        for (O = 0; O < A; O++) {
            const $ = u[O] = C ? Ye(u[O]) : De(u[O]);
            E(c[O], $, g, null, m, v, S, x, C)
        }
        b > M ? vt(c, m, v, !0, !1, A) : ee(u, g, y, m, v, S, x, C, A)
    }, Vt = (c, u, g, y, m, v, S, x, C) => {
        let b = 0;
        const M = u.length;
        let A = c.length - 1, O = M - 1;
        for (; b <= A && b <= O;) {
            const $ = c[b], D = u[b] = C ? Ye(u[b]) : De(u[b]);
            if (wt($, D)) E($, D, g, null, m, v, S, x, C); else break;
            b++
        }
        for (; b <= A && b <= O;) {
            const $ = c[A], D = u[O] = C ? Ye(u[O]) : De(u[O]);
            if (wt($, D)) E($, D, g, null, m, v, S, x, C); else break;
            A--, O--
        }
        if (b > A) {
            if (b <= O) {
                const $ = O + 1, D = $ < M ? u[$].el : y;
                for (; b <= O;) E(null, u[b] = C ? Ye(u[b]) : De(u[b]), g, D, m, v, S, x, C), b++
            }
        } else if (b > O) for (; b <= A;) Re(c[b], m, v, !0), b++; else {
            const $ = b, D = b, W = new Map;
            for (b = D; b <= O; b++) {
                const we = u[b] = C ? Ye(u[b]) : De(u[b]);
                we.key != null && W.set(we.key, b)
            }
            let K, ve = 0;
            const ye = O - D + 1;
            let $e = !1, Ie = 0;
            const bt = new Array(ye);
            for (b = 0; b < ye; b++) bt[b] = 0;
            for (b = $; b <= A; b++) {
                const we = c[b];
                if (ve >= ye) {
                    Re(we, m, v, !0);
                    continue
                }
                let Pe;
                if (we.key != null) Pe = W.get(we.key); else for (K = D; K <= O; K++) if (bt[K - D] === 0 && wt(we, u[K])) {
                    Pe = K;
                    break
                }
                Pe === void 0 ? Re(we, m, v, !0) : (bt[Pe - D] = b + 1, Pe >= Ie ? Ie = Pe : $e = !0, E(we, u[Pe], g, null, m, v, S, x, C), ve++)
            }
            const un = $e ? Ao(bt) : ut;
            for (K = un.length - 1, b = ye - 1; b >= 0; b--) {
                const we = D + b, Pe = u[we], dn = u[we + 1], hn = we + 1 < M ? dn.el || dn.placeholder : y;
                bt[b] === 0 ? E(null, Pe, g, hn, m, v, S, x, C) : $e && (K < 0 || b !== un[K] ? st(Pe, g, hn, 2) : K--)
            }
        }
    }, st = (c, u, g, y, m = null) => {
        const {el: v, type: S, transition: x, children: C, shapeFlag: b} = c;
        if (b & 6) {
            st(c.component.subTree, u, g, y);
            return
        }
        if (b & 128) {
            c.suspense.move(u, g, y);
            return
        }
        if (b & 64) {
            S.move(c, u, g, yt);
            return
        }
        if (S === fe) {
            n(v, u, g);
            for (let A = 0; A < C.length; A++) st(C[A], u, g, y);
            n(c.anchor, u, g);
            return
        }
        if (S === As) {
            U(c, u, g);
            return
        }
        if (y !== 2 && b & 1 && x) if (y === 0) x.beforeEnter(v), n(v, u, g), ge(() => x.enter(v), m); else {
            const {leave: A, delayLeave: O, afterLeave: $} = x, D = () => {
                c.ctx.isUnmounted ? r(v) : n(v, u, g)
            }, W = () => {
                A(v, () => {
                    D(), $ && $()
                })
            };
            O ? O(v, D, W) : W()
        } else n(v, u, g)
    }, Re = (c, u, g, y = !1, m = !1) => {
        const {
            type: v,
            props: S,
            ref: x,
            children: C,
            dynamicChildren: b,
            shapeFlag: M,
            patchFlag: A,
            dirs: O,
            cacheIndex: $
        } = c;
        if (A === -2 && (m = !1), x != null && (Ue(), Ot(x, null, g, c, !0), Ge()), $ != null && (u.renderCache[$] = void 0), M & 256) {
            u.ctx.deactivate(c);
            return
        }
        const D = M & 1 && O, W = !gt(c);
        let K;
        if (W && (K = S && S.onVnodeBeforeUnmount) && Fe(K, u, c), M & 6) el(c.component, g, y); else {
            if (M & 128) {
                c.suspense.unmount(g, y);
                return
            }
            D && nt(c, null, u, "beforeUnmount"), M & 64 ? c.type.remove(c, u, g, yt, y) : b && !b.hasOnce && (v !== fe || A > 0 && A & 64) ? vt(b, u, g, !1, !0) : (v === fe && A & 384 || !m && M & 16) && vt(C, u, g), y && fn(c)
        }
        (W && (K = S && S.onVnodeUnmounted) || D) && ge(() => {
            K && Fe(K, u, c), D && nt(c, null, u, "unmounted")
        }, g)
    }, fn = c => {
        const {type: u, el: g, anchor: y, transition: m} = c;
        if (u === fe) {
            Zr(g, y);
            return
        }
        if (u === As) {
            w(c);
            return
        }
        const v = () => {
            r(g), m && !m.persisted && m.afterLeave && m.afterLeave()
        };
        if (c.shapeFlag & 1 && m && !m.persisted) {
            const {leave: S, delayLeave: x} = m, C = () => S(g, v);
            x ? x(c.el, v, C) : C()
        } else v()
    }, Zr = (c, u) => {
        let g;
        for (; c !== u;) g = p(c), r(c), c = g;
        r(u)
    }, el = (c, u, g) => {
        const {bum: y, scope: m, job: v, subTree: S, um: x, m: C, a: b, parent: M, slots: {__: A}} = c;
        En(C), En(b), y && bs(y), M && I(A) && A.forEach(O => {
            M.renderCache[O] = void 0
        }), m.stop(), v && (v.flags |= 8, Re(S, c, u, g)), x && ge(x, u), ge(() => {
            c.isUnmounted = !0
        }, u), u && u.pendingBranch && !u.isUnmounted && c.asyncDep && !c.asyncResolved && c.suspenseId === u.pendingId && (u.deps--, u.deps === 0 && u.resolve())
    }, vt = (c, u, g, y = !1, m = !1, v = 0) => {
        for (let S = v; S < c.length; S++) Re(c[S], u, g, y, m)
    }, Ut = c => {
        if (c.shapeFlag & 6) return Ut(c.component.subTree);
        if (c.shapeFlag & 128) return c.suspense.next();
        const u = p(c.anchor || c.el), g = u && u[br];
        return g ? p(g) : u
    };
    let vs = !1;
    const an = (c, u, g) => {
        c == null ? u._vnode && Re(u._vnode, null, null, !0) : E(u._vnode || null, c, u, null, null, null, g), u._vnode = c, vs || (vs = !0, _n(), _r(), vs = !1)
    }, yt = {p: E, um: Re, m: st, r: fn, mt: se, mc: ee, pc: V, pbc: le, n: Ut, o: e};
    return {render: an, hydrate: void 0, createApp: mo(an)}
}

function Es({type: e, props: t}, s) {
    return s === "svg" && e === "foreignObject" || s === "mathml" && e === "annotation-xml" && t && t.encoding && t.encoding.includes("html") ? void 0 : s
}

function rt({effect: e, job: t}, s) {
    s ? (e.flags |= 32, t.flags |= 4) : (e.flags &= -33, t.flags &= -5)
}

function Eo(e, t) {
    return (!e || e && !e.pendingBranch) && t && !t.persisted
}

function rn(e, t, s = !1) {
    const n = e.children, r = t.children;
    if (I(n) && I(r)) for (let l = 0; l < n.length; l++) {
        const o = n[l];
        let i = r[l];
        i.shapeFlag & 1 && !i.dynamicChildren && ((i.patchFlag <= 0 || i.patchFlag === 32) && (i = r[l] = Ye(r[l]), i.el = o.el), !s && i.patchFlag !== -2 && rn(o, i)), i.type === _s && (i.el = o.el), i.type === We && !i.el && (i.el = o.el)
    }
}

function Ao(e) {
    const t = e.slice(), s = [0];
    let n, r, l, o, i;
    const f = e.length;
    for (n = 0; n < f; n++) {
        const d = e[n];
        if (d !== 0) {
            if (r = s[s.length - 1], e[r] < d) {
                t[n] = r, s.push(n);
                continue
            }
            for (l = 0, o = s.length - 1; l < o;) i = l + o >> 1, e[s[i]] < d ? l = i + 1 : o = i;
            d < e[s[l]] && (l > 0 && (t[n] = s[l - 1]), s[l] = n)
        }
    }
    for (l = s.length, o = s[l - 1]; l-- > 0;) s[l] = o, o = t[o];
    return s
}

function kr(e) {
    const t = e.subTree.component;
    if (t) return t.asyncDep && !t.asyncResolved ? t : kr(t)
}

function En(e) {
    if (e) for (let t = 0; t < e.length; t++) e[t].flags |= 8
}

const Oo = Symbol.for("v-scx"), Mo = () => Qt(Oo);

function Rt(e, t, s) {
    return Hr(e, t, s)
}

function Hr(e, t, s = z) {
    const {immediate: n, deep: r, flush: l, once: o} = s, i = de({}, s), f = t && n || !t && l !== "post";
    let d;
    if (Lt) {
        if (l === "sync") {
            const _ = Mo();
            d = _.__watcherHandles || (_.__watcherHandles = [])
        } else if (!f) {
            const _ = () => {
            };
            return _.stop = Le, _.resume = Le, _.pause = Le, _
        }
    }
    const a = _e;
    i.call = (_, T, E) => ke(_, a, T, E);
    let h = !1;
    l === "post" ? i.scheduler = _ => {
        ge(_, a && a.suspense)
    } : l !== "sync" && (h = !0, i.scheduler = (_, T) => {
        T ? _() : en(_)
    }), i.augmentJob = _ => {
        t && (_.flags |= 4), h && (_.flags |= 2, a && (_.id = a.uid, _.i = a))
    };
    const p = Bl(e, t, i);
    return Lt && (d ? d.push(p) : f && p()), p
}

function Ro(e, t, s) {
    const n = this.proxy, r = te(e) ? e.includes(".") ? jr(n, e) : () => n[e] : e.bind(n, n);
    let l;
    P(t) ? l = t : (l = t.handler, s = t);
    const o = Bt(this), i = Hr(r, l.bind(n), s);
    return o(), i
}

function jr(e, t) {
    const s = t.split(".");
    return () => {
        let n = e;
        for (let r = 0; r < s.length && n; r++) n = n[s[r]];
        return n
    }
}

const $o = (e, t) => t === "modelValue" || t === "model-value" ? e.modelModifiers : e[`${t}Modifiers`] || e[`${Ze(t)}Modifiers`] || e[`${ct(t)}Modifiers`];

function Io(e, t, ...s) {
    if (e.isUnmounted) return;
    const n = e.vnode.props || z;
    let r = s;
    const l = t.startsWith("update:"), o = l && $o(n, t.slice(7));
    o && (o.trim && (r = s.map(a => te(a) ? a.trim() : a)), o.number && (r = s.map(ol)));
    let i, f = n[i = ys(t)] || n[i = ys(Ze(t))];
    !f && l && (f = n[i = ys(ct(t))]), f && ke(f, e, 6, r);
    const d = n[i + "Once"];
    if (d) {
        if (!e.emitted) e.emitted = {}; else if (e.emitted[i]) return;
        e.emitted[i] = !0, ke(d, e, 6, r)
    }
}

function Br(e, t, s = !1) {
    const n = t.emitsCache, r = n.get(e);
    if (r !== void 0) return r;
    const l = e.emits;
    let o = {}, i = !1;
    if (!P(e)) {
        const f = d => {
            const a = Br(d, t, !0);
            a && (i = !0, de(o, a))
        };
        !s && t.mixins.length && t.mixins.forEach(f), e.extends && f(e.extends), e.mixins && e.mixins.forEach(f)
    }
    return !l && !i ? (X(e) && n.set(e, null), null) : (I(l) ? l.forEach(f => o[f] = null) : de(o, l), X(e) && n.set(e, o), o)
}

function ms(e, t) {
    return !e || !os(t) ? !1 : (t = t.slice(2).replace(/Once$/, ""), B(e, t[0].toLowerCase() + t.slice(1)) || B(e, ct(t)) || B(e, t))
}

function An(e) {
    const {
        type: t,
        vnode: s,
        proxy: n,
        withProxy: r,
        propsOptions: [l],
        slots: o,
        attrs: i,
        emit: f,
        render: d,
        renderCache: a,
        props: h,
        data: p,
        setupState: _,
        ctx: T,
        inheritAttrs: E
    } = e, k = ns(e);
    let R, L;
    try {
        if (s.shapeFlag & 4) {
            const w = r || n, N = w;
            R = De(d.call(N, w, a, h, _, p, T)), L = i
        } else {
            const w = t;
            R = De(w.length > 1 ? w(h, {attrs: i, slots: o, emit: f}) : w(h, null)), L = t.props ? i : Po(i)
        }
    } catch (w) {
        $t.length = 0, ds(w, e, 1), R = Me(We)
    }
    let U = R;
    if (L && E !== !1) {
        const w = Object.keys(L), {shapeFlag: N} = U;
        w.length && N & 7 && (l && w.some(Vs) && (L = Fo(L, l)), U = _t(U, L, !1, !0))
    }
    return s.dirs && (U = _t(U, null, !1, !0), U.dirs = U.dirs ? U.dirs.concat(s.dirs) : s.dirs), s.transition && tn(U, s.transition), R = U, ns(k), R
}

const Po = e => {
    let t;
    for (const s in e) (s === "class" || s === "style" || os(s)) && ((t || (t = {}))[s] = e[s]);
    return t
}, Fo = (e, t) => {
    const s = {};
    for (const n in e) (!Vs(n) || !(n.slice(9) in t)) && (s[n] = e[n]);
    return s
};

function No(e, t, s) {
    const {props: n, children: r, component: l} = e, {props: o, children: i, patchFlag: f} = t, d = l.emitsOptions;
    if (t.dirs || t.transition) return !0;
    if (s && f >= 0) {
        if (f & 1024) return !0;
        if (f & 16) return n ? On(n, o, d) : !!o;
        if (f & 8) {
            const a = t.dynamicProps;
            for (let h = 0; h < a.length; h++) {
                const p = a[h];
                if (o[p] !== n[p] && !ms(d, p)) return !0
            }
        }
    } else return (r || i) && (!i || !i.$stable) ? !0 : n === o ? !1 : n ? o ? On(n, o, d) : !0 : !!o;
    return !1
}

function On(e, t, s) {
    const n = Object.keys(t);
    if (n.length !== Object.keys(e).length) return !0;
    for (let r = 0; r < n.length; r++) {
        const l = n[r];
        if (t[l] !== e[l] && !ms(s, l)) return !0
    }
    return !1
}

function Do({vnode: e, parent: t}, s) {
    for (; t;) {
        const n = t.subTree;
        if (n.suspense && n.suspense.activeBranch === e && (n.el = e.el), n === e) (e = t.vnode).el = s, t = t.parent; else break
    }
}

const Kr = e => e.__isSuspense;

function Lo(e, t) {
    t && t.pendingBranch ? I(e) ? t.effects.push(...e) : t.effects.push(e) : Ul(e)
}

const fe = Symbol.for("v-fgt"), _s = Symbol.for("v-txt"), We = Symbol.for("v-cmt"), As = Symbol.for("v-stc"), $t = [];
let xe = null;

function Q(e = !1) {
    $t.push(xe = e ? null : [])
}

function ko() {
    $t.pop(), xe = $t[$t.length - 1] || null
}

let Nt = 1;

function Mn(e, t = !1) {
    Nt += e, e < 0 && xe && t && (xe.hasOnce = !0)
}

function Vr(e) {
    return e.dynamicChildren = Nt > 0 ? xe || ut : null, ko(), Nt > 0 && xe && xe.push(e), e
}

function ae(e, t, s, n, r, l) {
    return Vr(F(e, t, s, n, r, l, !0))
}

function it(e, t, s, n, r) {
    return Vr(Me(e, t, s, n, r, !0))
}

function ln(e) {
    return e ? e.__v_isVNode === !0 : !1
}

function wt(e, t) {
    return e.type === t.type && e.key === t.key
}

const Ur = ({key: e}) => e ?? null, Xt = ({
                                              ref: e,
                                              ref_key: t,
                                              ref_for: s
                                          }) => (typeof e == "number" && (e = "" + e), e != null ? te(e) || ue(e) || P(e) ? {
    i: Ce,
    r: e,
    k: t,
    f: !!s
} : e : null);

function F(e, t = null, s = null, n = 0, r = null, l = e === fe ? 0 : 1, o = !1, i = !1) {
    const f = {
        __v_isVNode: !0,
        __v_skip: !0,
        type: e,
        props: t,
        key: t && Ur(t),
        ref: t && Xt(t),
        scopeId: yr,
        slotScopeIds: null,
        children: s,
        component: null,
        suspense: null,
        ssContent: null,
        ssFallback: null,
        dirs: null,
        transition: null,
        el: null,
        anchor: null,
        target: null,
        targetStart: null,
        targetAnchor: null,
        staticCount: 0,
        shapeFlag: l,
        patchFlag: n,
        dynamicProps: r,
        dynamicChildren: null,
        appContext: null,
        ctx: Ce
    };
    return i ? (on(f, s), l & 128 && e.normalize(f)) : s && (f.shapeFlag |= te(s) ? 8 : 16), Nt > 0 && !o && xe && (f.patchFlag > 0 || l & 6) && f.patchFlag !== 32 && xe.push(f), f
}

const Me = Ho;

function Ho(e, t = null, s = null, n = 0, r = null, l = !1) {
    if ((!e || e === oo) && (e = We), ln(e)) {
        const i = _t(e, t, !0);
        return s && on(i, s), Nt > 0 && !l && xe && (i.shapeFlag & 6 ? xe[xe.indexOf(e)] = i : xe.push(i)), i.patchFlag = -2, i
    }
    if (Yo(e) && (e = e.__vccOpts), t) {
        t = jo(t);
        let {class: i, style: f} = t;
        i && !te(i) && (t.class = as(i)), X(f) && (Zs(f) && !I(f) && (f = de({}, f)), t.style = Ws(f))
    }
    const o = te(e) ? 1 : Kr(e) ? 128 : Wl(e) ? 64 : X(e) ? 4 : P(e) ? 2 : 0;
    return F(e, t, s, n, r, o, l, !0)
}

function jo(e) {
    return e ? Zs(e) || Ir(e) ? de({}, e) : e : null
}

function _t(e, t, s = !1, n = !1) {
    const {props: r, ref: l, patchFlag: o, children: i, transition: f} = e, d = t ? Bo(r || {}, t) : r, a = {
        __v_isVNode: !0,
        __v_skip: !0,
        type: e.type,
        props: d,
        key: d && Ur(d),
        ref: t && t.ref ? s && l ? I(l) ? l.concat(Xt(t)) : [l, Xt(t)] : Xt(t) : l,
        scopeId: e.scopeId,
        slotScopeIds: e.slotScopeIds,
        children: i,
        target: e.target,
        targetStart: e.targetStart,
        targetAnchor: e.targetAnchor,
        staticCount: e.staticCount,
        shapeFlag: e.shapeFlag,
        patchFlag: t && e.type !== fe ? o === -1 ? 16 : o | 16 : o,
        dynamicProps: e.dynamicProps,
        dynamicChildren: e.dynamicChildren,
        appContext: e.appContext,
        dirs: e.dirs,
        transition: f,
        component: e.component,
        suspense: e.suspense,
        ssContent: e.ssContent && _t(e.ssContent),
        ssFallback: e.ssFallback && _t(e.ssFallback),
        placeholder: e.placeholder,
        el: e.el,
        anchor: e.anchor,
        ctx: e.ctx,
        ce: e.ce
    };
    return f && n && tn(a, f.clone(a)), a
}

function Be(e = " ", t = 0) {
    return Me(_s, null, e, t)
}

function Dt(e = "", t = !1) {
    return t ? (Q(), it(We, null, e)) : Me(We, null, e)
}

function De(e) {
    return e == null || typeof e == "boolean" ? Me(We) : I(e) ? Me(fe, null, e.slice()) : ln(e) ? Ye(e) : Me(_s, null, String(e))
}

function Ye(e) {
    return e.el === null && e.patchFlag !== -1 || e.memo ? e : _t(e)
}

function on(e, t) {
    let s = 0;
    const {shapeFlag: n} = e;
    if (t == null) t = null; else if (I(t)) s = 16; else if (typeof t == "object") if (n & 65) {
        const r = t.default;
        r && (r._c && (r._d = !1), on(e, r()), r._c && (r._d = !0));
        return
    } else {
        s = 32;
        const r = t._;
        !r && !Ir(t) ? t._ctx = Ce : r === 3 && Ce && (Ce.slots._ === 1 ? t._ = 1 : (t._ = 2, e.patchFlag |= 1024))
    } else P(t) ? (t = {default: t, _ctx: Ce}, s = 32) : (t = String(t), n & 64 ? (s = 16, t = [Be(t)]) : s = 8);
    e.children = t, e.shapeFlag |= s
}

function Bo(...e) {
    const t = {};
    for (let s = 0; s < e.length; s++) {
        const n = e[s];
        for (const r in n) if (r === "class") t.class !== n.class && (t.class = as([t.class, n.class])); else if (r === "style") t.style = Ws([t.style, n.style]); else if (os(r)) {
            const l = t[r], o = n[r];
            o && l !== o && !(I(l) && l.includes(o)) && (t[r] = l ? [].concat(l, o) : o)
        } else r !== "" && (t[r] = n[r])
    }
    return t
}

function Fe(e, t, s, n = null) {
    ke(e, t, 7, [s, n])
}

const Ko = Mr();
let Vo = 0;

function Uo(e, t, s) {
    const n = e.type, r = (t ? t.appContext : e.appContext) || Ko, l = {
        uid: Vo++,
        vnode: e,
        type: n,
        parent: t,
        appContext: r,
        root: null,
        next: null,
        subTree: null,
        effect: null,
        update: null,
        job: null,
        scope: new hl(!0),
        render: null,
        proxy: null,
        exposed: null,
        exposeProxy: null,
        withProxy: null,
        provides: t ? t.provides : Object.create(r.provides),
        ids: t ? t.ids : ["", 0, 0],
        accessCache: null,
        renderCache: [],
        components: null,
        directives: null,
        propsOptions: Fr(n, r),
        emitsOptions: Br(n, r),
        emit: null,
        emitted: null,
        propsDefaults: z,
        inheritAttrs: n.inheritAttrs,
        ctx: z,
        data: z,
        props: z,
        attrs: z,
        slots: z,
        refs: z,
        setupState: z,
        setupContext: null,
        suspense: s,
        suspenseId: s ? s.pendingId : 0,
        asyncDep: null,
        asyncResolved: !1,
        isMounted: !1,
        isUnmounted: !1,
        isDeactivated: !1,
        bc: null,
        c: null,
        bm: null,
        m: null,
        bu: null,
        u: null,
        um: null,
        bum: null,
        da: null,
        a: null,
        rtg: null,
        rtc: null,
        ec: null,
        sp: null
    };
    return l.ctx = {_: l}, l.root = t ? t.root : l, l.emit = Io.bind(null, l), e.ce && e.ce(l), l
}

let _e = null;
const Go = () => _e || Ce;
let ls, js;
{
    const e = fs(), t = (s, n) => {
        let r;
        return (r = e[s]) || (r = e[s] = []), r.push(n), l => {
            r.length > 1 ? r.forEach(o => o(l)) : r[0](l)
        }
    };
    ls = t("__VUE_INSTANCE_SETTERS__", s => _e = s), js = t("__VUE_SSR_SETTERS__", s => Lt = s)
}
const Bt = e => {
    const t = _e;
    return ls(e), e.scope.on(), () => {
        e.scope.off(), ls(t)
    }
}, Rn = () => {
    _e && _e.scope.off(), ls(null)
};

function Gr(e) {
    return e.vnode.shapeFlag & 4
}

let Lt = !1;

function Wo(e, t = !1, s = !1) {
    t && js(t);
    const {props: n, children: r} = e.vnode, l = Gr(e);
    vo(e, n, l, t), wo(e, r, s || t);
    const o = l ? qo(e, t) : void 0;
    return t && js(!1), o
}

function qo(e, t) {
    const s = e.type;
    e.accessCache = Object.create(null), e.proxy = new Proxy(e.ctx, co);
    const {setup: n} = s;
    if (n) {
        Ue();
        const r = e.setupContext = n.length > 1 ? Jo(e) : null, l = Bt(e), o = Ht(n, e, 0, [e.props, r]), i = Gn(o);
        if (Ge(), l(), (i || e.sp) && !gt(e) && xr(e), i) {
            if (o.then(Rn, Rn), t) return o.then(f => {
                $n(e, f)
            }).catch(f => {
                ds(f, e, 0)
            });
            e.asyncDep = o
        } else $n(e, o)
    } else Wr(e)
}

function $n(e, t, s) {
    P(t) ? e.type.__ssrInlineRender ? e.ssrRender = t : e.render = t : X(t) && (e.setupState = hr(t)), Wr(e)
}

function Wr(e, t, s) {
    const n = e.type;
    e.render || (e.render = n.render || Le);
    {
        const r = Bt(e);
        Ue();
        try {
            fo(e)
        } finally {
            Ge(), r()
        }
    }
}

const zo = {
    get(e, t) {
        return ce(e, "get", ""), e[t]
    }
};

function Jo(e) {
    const t = s => {
        e.exposed = s || {}
    };
    return {attrs: new Proxy(e.attrs, zo), slots: e.slots, emit: e.emit, expose: t}
}

function cn(e) {
    return e.exposed ? e.exposeProxy || (e.exposeProxy = new Proxy(hr(Fl(e.exposed)), {
        get(t, s) {
            if (s in t) return t[s];
            if (s in Mt) return Mt[s](e)
        }, has(t, s) {
            return s in t || s in Mt
        }
    })) : e.proxy
}

function Yo(e) {
    return P(e) && "__vccOpts" in e
}

const Ke = (e, t) => Hl(e, t, Lt), Qo = "3.5.18";
/**
 * @vue/runtime-dom v3.5.18
 * (c) 2018-present Yuxi (Evan) You and Vue contributors
 * @license MIT
 **/let Bs;
const In = typeof window < "u" && window.trustedTypes;
if (In) try {
    Bs = In.createPolicy("vue", {createHTML: e => e})
} catch {
}
const qr = Bs ? e => Bs.createHTML(e) : e => e, Xo = "http://www.w3.org/2000/svg",
    Zo = "http://www.w3.org/1998/Math/MathML", je = typeof document < "u" ? document : null,
    Pn = je && je.createElement("template"), ei = {
        insert: (e, t, s) => {
            t.insertBefore(e, s || null)
        },
        remove: e => {
            const t = e.parentNode;
            t && t.removeChild(e)
        },
        createElement: (e, t, s, n) => {
            const r = t === "svg" ? je.createElementNS(Xo, e) : t === "mathml" ? je.createElementNS(Zo, e) : s ? je.createElement(e, {is: s}) : je.createElement(e);
            return e === "select" && n && n.multiple != null && r.setAttribute("multiple", n.multiple), r
        },
        createText: e => je.createTextNode(e),
        createComment: e => je.createComment(e),
        setText: (e, t) => {
            e.nodeValue = t
        },
        setElementText: (e, t) => {
            e.textContent = t
        },
        parentNode: e => e.parentNode,
        nextSibling: e => e.nextSibling,
        querySelector: e => je.querySelector(e),
        setScopeId(e, t) {
            e.setAttribute(t, "")
        },
        insertStaticContent(e, t, s, n, r, l) {
            const o = s ? s.previousSibling : t.lastChild;
            if (r && (r === l || r.nextSibling)) for (; t.insertBefore(r.cloneNode(!0), s), !(r === l || !(r = r.nextSibling));) ; else {
                Pn.innerHTML = qr(n === "svg" ? `<svg>${e}</svg>` : n === "mathml" ? `<math>${e}</math>` : e);
                const i = Pn.content;
                if (n === "svg" || n === "mathml") {
                    const f = i.firstChild;
                    for (; f.firstChild;) i.appendChild(f.firstChild);
                    i.removeChild(f)
                }
                t.insertBefore(i, s)
            }
            return [o ? o.nextSibling : t.firstChild, s ? s.previousSibling : t.lastChild]
        }
    }, ti = Symbol("_vtc");

function si(e, t, s) {
    const n = e[ti];
    n && (t = (t ? [t, ...n] : [...n]).join(" ")), t == null ? e.removeAttribute("class") : s ? e.setAttribute("class", t) : e.className = t
}

const Fn = Symbol("_vod"), ni = Symbol("_vsh"), ri = Symbol(""), li = /(^|;)\s*display\s*:/;

function oi(e, t, s) {
    const n = e.style, r = te(s);
    let l = !1;
    if (s && !r) {
        if (t) if (te(t)) for (const o of t.split(";")) {
            const i = o.slice(0, o.indexOf(":")).trim();
            s[i] == null && Zt(n, i, "")
        } else for (const o in t) s[o] == null && Zt(n, o, "");
        for (const o in s) o === "display" && (l = !0), Zt(n, o, s[o])
    } else if (r) {
        if (t !== s) {
            const o = n[ri];
            o && (s += ";" + o), n.cssText = s, l = li.test(s)
        }
    } else t && e.removeAttribute("style");
    Fn in e && (e[Fn] = l ? n.display : "", e[ni] && (n.display = "none"))
}

const Nn = /\s*!important$/;

function Zt(e, t, s) {
    if (I(s)) s.forEach(n => Zt(e, t, n)); else if (s == null && (s = ""), t.startsWith("--")) e.setProperty(t, s); else {
        const n = ii(e, t);
        Nn.test(s) ? e.setProperty(ct(n), s.replace(Nn, ""), "important") : e[n] = s
    }
}

const Dn = ["Webkit", "Moz", "ms"], Os = {};

function ii(e, t) {
    const s = Os[t];
    if (s) return s;
    let n = Ze(t);
    if (n !== "filter" && n in e) return Os[t] = n;
    n = zn(n);
    for (let r = 0; r < Dn.length; r++) {
        const l = Dn[r] + n;
        if (l in e) return Os[t] = l
    }
    return t
}

const Ln = "http://www.w3.org/1999/xlink";

function kn(e, t, s, n, r, l = dl(t)) {
    n && t.startsWith("xlink:") ? s == null ? e.removeAttributeNS(Ln, t.slice(6, t.length)) : e.setAttributeNS(Ln, t, s) : s == null || l && !Jn(s) ? e.removeAttribute(t) : e.setAttribute(t, l ? "" : qe(s) ? String(s) : s)
}

function Hn(e, t, s, n, r) {
    if (t === "innerHTML" || t === "textContent") {
        s != null && (e[t] = t === "innerHTML" ? qr(s) : s);
        return
    }
    const l = e.tagName;
    if (t === "value" && l !== "PROGRESS" && !l.includes("-")) {
        const i = l === "OPTION" ? e.getAttribute("value") || "" : e.value,
            f = s == null ? e.type === "checkbox" ? "on" : "" : String(s);
        (i !== f || !("_value" in e)) && (e.value = f), s == null && e.removeAttribute(t), e._value = s;
        return
    }
    let o = !1;
    if (s === "" || s == null) {
        const i = typeof e[t];
        i === "boolean" ? s = Jn(s) : s == null && i === "string" ? (s = "", o = !0) : i === "number" && (s = 0, o = !0)
    }
    try {
        e[t] = s
    } catch {
    }
    o && e.removeAttribute(r || t)
}

function ci(e, t, s, n) {
    e.addEventListener(t, s, n)
}

function fi(e, t, s, n) {
    e.removeEventListener(t, s, n)
}

const jn = Symbol("_vei");

function ai(e, t, s, n, r = null) {
    const l = e[jn] || (e[jn] = {}), o = l[t];
    if (n && o) o.value = n; else {
        const [i, f] = ui(t);
        if (n) {
            const d = l[t] = pi(n, r);
            ci(e, i, d, f)
        } else o && (fi(e, i, o, f), l[t] = void 0)
    }
}

const Bn = /(?:Once|Passive|Capture)$/;

function ui(e) {
    let t;
    if (Bn.test(e)) {
        t = {};
        let n;
        for (; n = e.match(Bn);) e = e.slice(0, e.length - n[0].length), t[n[0].toLowerCase()] = !0
    }
    return [e[2] === ":" ? e.slice(3) : ct(e.slice(2)), t]
}

let Ms = 0;
const di = Promise.resolve(), hi = () => Ms || (di.then(() => Ms = 0), Ms = Date.now());

function pi(e, t) {
    const s = n => {
        if (!n._vts) n._vts = Date.now(); else if (n._vts <= s.attached) return;
        ke(gi(n, s.value), t, 5, [n])
    };
    return s.value = e, s.attached = hi(), s
}

function gi(e, t) {
    if (I(t)) {
        const s = e.stopImmediatePropagation;
        return e.stopImmediatePropagation = () => {
            s.call(e), e._stopped = !0
        }, t.map(n => r => !r._stopped && n && n(r))
    } else return t
}

const Kn = e => e.charCodeAt(0) === 111 && e.charCodeAt(1) === 110 && e.charCodeAt(2) > 96 && e.charCodeAt(2) < 123,
    mi = (e, t, s, n, r, l) => {
        const o = r === "svg";
        t === "class" ? si(e, n, o) : t === "style" ? oi(e, s, n) : os(t) ? Vs(t) || ai(e, t, s, n, l) : (t[0] === "." ? (t = t.slice(1), !0) : t[0] === "^" ? (t = t.slice(1), !1) : _i(e, t, n, o)) ? (Hn(e, t, n), !e.tagName.includes("-") && (t === "value" || t === "checked" || t === "selected") && kn(e, t, n, o, l, t !== "value")) : e._isVueCE && (/[A-Z]/.test(t) || !te(n)) ? Hn(e, Ze(t), n, l, t) : (t === "true-value" ? e._trueValue = n : t === "false-value" && (e._falseValue = n), kn(e, t, n, o))
    };

function _i(e, t, s, n) {
    if (n) return !!(t === "innerHTML" || t === "textContent" || t in e && Kn(t) && P(s));
    if (t === "spellcheck" || t === "draggable" || t === "translate" || t === "autocorrect" || t === "form" || t === "list" && e.tagName === "INPUT" || t === "type" && e.tagName === "TEXTAREA") return !1;
    if (t === "width" || t === "height") {
        const r = e.tagName;
        if (r === "IMG" || r === "VIDEO" || r === "CANVAS" || r === "SOURCE") return !1
    }
    return Kn(t) && te(s) ? !1 : t in e
}

const vi = ["ctrl", "shift", "alt", "meta"], yi = {
    stop: e => e.stopPropagation(),
    prevent: e => e.preventDefault(),
    self: e => e.target !== e.currentTarget,
    ctrl: e => !e.ctrlKey,
    shift: e => !e.shiftKey,
    alt: e => !e.altKey,
    meta: e => !e.metaKey,
    left: e => "button" in e && e.button !== 0,
    middle: e => "button" in e && e.button !== 1,
    right: e => "button" in e && e.button !== 2,
    exact: (e, t) => vi.some(s => e[`${s}Key`] && !t.includes(s))
}, bi = (e, t) => {
    const s = e._withMods || (e._withMods = {}), n = t.join(".");
    return s[n] || (s[n] = (r, ...l) => {
        for (let o = 0; o < t.length; o++) {
            const i = yi[t[o]];
            if (i && i(r, t)) return
        }
        return e(r, ...l)
    })
}, Ci = de({patchProp: mi}, ei);
let Vn;

function wi() {
    return Vn || (Vn = To(Ci))
}

const xi = (...e) => {
    const t = wi().createApp(...e), {mount: s} = t;
    return t.mount = n => {
        const r = Si(n);
        if (!r) return;
        const l = t._component;
        !P(l) && !l.render && !l.template && (l.template = r.innerHTML), r.nodeType === 1 && (r.textContent = "");
        const o = s(r, !1, Ti(r));
        return r instanceof Element && (r.removeAttribute("v-cloak"), r.setAttribute("data-v-app", "")), o
    }, t
};

function Ti(e) {
    if (e instanceof SVGElement) return "svg";
    if (typeof MathMLElement == "function" && e instanceof MathMLElement) return "mathml"
}

function Si(e) {
    return te(e) ? document.querySelector(e) : e
}

function Ei() {
    const e = re(null), t = re([]), s = re(!1), n = re(null), r = async () => {
        try {
            const a = await fetch("/api/metadata");
            if (!a.ok) throw new Error(`Failed to load metadata: ${a.statusText}`);
            const h = await a.json();
            return e.value = h, h
        } catch (a) {
            const h = a instanceof Error ? a.message : "Unknown error loading metadata";
            throw n.value = h, new Error(h)
        }
    }, l = async (a, h, p, _) => {
        try {
            const T = await fetch("/api/click", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({boardName: a, x: h, y: p, button: _})
            });
            if (!T.ok) throw new Error(`Failed to post click: ${T.statusText}`);
            const E = await T.json();
            return t.value = E.cells, E
        } catch (T) {
            const E = T instanceof Error ? T.message : "Unknown error posting click";
            throw n.value = E, new Error(E)
        }
    }, o = a => {
        const h = {};
        for (const [p, [_, T]] of Object.entries(a.boards)) {
            const E = kt({});
            for (let k = 0; k < _; k++) for (let R = 0; R < T; R++) {
                const L = `${k}-${R}`;
                E[L] = {type: "empty", value: null, isRevealed: !1}
            }
            h[p] = E
        }
        return h
    }, i = (a, h) => {
        for (const p of h) {
            const {position: _, component: T} = p, E = a[_.boardname];
            if (!E) {
                console.warn(`Board ${_.boardname} not found`);
                continue
            }
            const k = `${_.x}-${_.y}`, R = E[k];
            if (!R) {
                console.warn(`Cell ${k} not found in board ${_.boardname}`);
                continue
            }
            R.type = "revealed", R.isRevealed = !0, R.value = T
        }
    };
    return {
        metadata: e,
        additionalCells: t,
        isLoading: s,
        error: n,
        loadMetadata: r,
        postClick: l,
        createGameBoards: o,
        applyCellConfigs: i,
        getCellHighlight: (a, h, p, _) => a.some(T => !T.highlight || !T.highlight[h] ? !1 : T.highlight[h].some(([E, k]) => E === p && k === _)),
        loadGameConfig: async () => {
            s.value = !0, n.value = null;
            try {
                const a = await r(), h = [...a.cells], p = o(a);
                return i(p, h), {metadata: a, boards: p, allCells: h}
            } catch (a) {
                throw console.error("Failed to load game config:", a), a
            } finally {
                s.value = !1
            }
        }
    }
}

function zr(e) {
    if (e < 0) throw new Error("Index cannot be negative");
    let t = "", s = e;
    do t = String.fromCharCode(65 + s % 26) + t, s = Math.floor(s / 26) - 1; while (s >= 0);
    return t
}

function Jr(e) {
    if (!e || typeof e != "string") throw new Error("Column must be a non-empty string");
    const t = e.toUpperCase();
    let s = 0;
    for (let n = 0; n < t.length; n++) {
        const r = t.charCodeAt(n);
        if (r < 65 || r > 90) throw new Error(`Invalid character in column: ${e}`);
        s = s * 26 + (r - 65 + 1)
    }
    return s - 1
}

function Ai(e) {
    return Array.from({length: e}, (t, s) => zr(s))
}

function Oi(e) {
    return Array.from({length: e}, (t, s) => s + 1)
}

function Yr(e, t) {
    const s = e - 1, n = Jr(t);
    return `${s}-${n}`
}

function Qr(e, t) {
    return {x: e - 1, y: Jr(t)}
}

function Mi(e, t) {
    return {row: e + 1, col: zr(t)}
}

function Ri() {
    const {loadGameConfig: e, postClick: t} = Ei(), s = re({}), n = re(null), r = re([]), l = re(!1), o = re(!1),
        i = re(null), f = re(!1), d = re(""), a = async () => {
            o.value = !0, i.value = null, f.value = !1, d.value = "";
            try {
                const w = await e();
                s.value = w.boards, n.value = w.metadata, r.value = w.allCells, l.value = !0, console.log("Game initialized with config:", {
                    metadata: w.metadata,
                    boards: Object.keys(w.boards),
                    cellCount: w.allCells.length
                })
            } catch (w) {
                const N = w instanceof Error ? w.message : "Failed to initialize game";
                i.value = N, console.error("Game initialization failed:", w)
            } finally {
                o.value = !1
            }
        }, h = w => s.value[w] || kt({}), p = w => {
            if (!n.value) return {rows: [], cols: []};
            const N = n.value.boards[w];
            return N ? {rows: Oi(N[0]), cols: Ai(N[1])} : {rows: [], cols: []}
        }, _ = async (w, N, J) => {
            if (f.value) {
                console.log("Game is over, click ignored");
                return
            }
            const Y = h(w), ee = Yr(N, J), G = Y[ee];
            console.log(`Cell clicked: Board ${w}, Position ${ee} (row: ${N}, col: ${J})`, G);
            const {x: le, y: he} = Qr(N, J), Ee = T(w, le, he);
            // if (Ee && Ee.clickable === !1) {
            //     console.log("Cell is not clickable according to configuration");
            //     return
            // }
            if (G && G.type === "empty" && !G.isRevealed) try {
                const Z = await t(w, le, he, "left");
                if (!Z.success) {
                    console.error("Click failed:", Z.reason);
                    return
                }
                if (Z.cells && Z.cells.length > 0) {
                    for (const se of Z.cells) {
                        const oe = s.value[se.position.boardname];
                        if (oe) {
                            const ne = `${se.position.x}-${se.position.y}`, H = oe[ne];
                            H && (H.type = "revealed", H.isRevealed = !0, H.value = se.component)
                        }
                    }
                    r.value = [...r.value, ...Z.cells]
                } else {
                    const se = Math.floor(Math.random() * 3) + 1;
                    G.type = "revealed", G.value = se.toString(), G.isRevealed = !0
                }
                Z.gameover && (f.value = !0, d.value = Z.reason, console.log("Game over:", Z.reason))
            } catch (Z) {
                console.error("Failed to post click:", Z)
            }
        },
        T = (w, N, J) => r.value && r.value.find(Y => Y.position.boardname === w && Y.position.x === N && Y.position.y === J) || null,
        E = async () => {
            await a()
        }, k = () => n.value?.rules || [], R = () => n.value ? Object.keys(n.value.boards) : [],
        L = w => n.value ? {name: w, size: n.value.boards[w], gameBoard: h(w), labels: p(w)} : null;
    return {
        gameBoards: s,
        metadata: n,
        allCells: r,
        isInitialized: l,
        isLoading: o,
        error: i,
        isGameOver: f,
        gameOverReason: d,
        initializeGame: a,
        getGameBoard: h,
        getBoardLabels: p,
        handleCellClick: _,
        getCellConfig: T,
        resetGame: E,
        getGameRules: k,
        getBoardNames: R,
        getBoardConfig: L,
        getAllBoardConfigs: () => R().map(w => L(w)).filter(Boolean)
    }
}

function Xr() {
    const e = re({flag: null, star: null, circle: null, cross: null, arrow: null, double_arrow: null}), t = re(!1),
        s = re(null), n = async () => {
            const i = Object.entries({
                flag: "/assets/flag.svg",
                star: "/assets/star.svg",
                circle: "/assets/circle.svg",
                cross: "/assets/cross.svg",
                arrow: "/assets/arrow.svg",
                double_arrow: "/assets/double_arrow.svg"
            }).map(async ([f, d]) => {
                try {
                    const a = await fetch(d);
                    if (!a.ok) throw new Error(`Failed to load ${d}: ${a.status}`);
                    const h = await a.text(), T = new DOMParser().parseFromString(h, "image/svg+xml").documentElement;
                    if (T.tagName === "svg") return e.value[f] = T, console.log(`Successfully loaded SVG: ${f}`), {
                        name: f,
                        success: !0
                    };
                    throw new Error(`Invalid SVG format in ${d}`)
                } catch (a) {
                    return console.warn(`Failed to load ${f} SVG:`, a), e.value[f] = null, {name: f, success: !1, error: a}
                }
            });
            return await Promise.all(i), t.value = !0, console.log("All SVG assets loading completed"), e.value
        }, r = async () => t.value ? e.value : (s.value || (s.value = n()), s.value), l = async o => {
            await r();
            const i = e.value[o];
            return i ? i.cloneNode(!0) : null
        };
    return ps(() => {
        n()
    }), {assetTemplates: e, assetsLoaded: t, cloneAsset: l, waitForAssets: r}
}

function $i() {
    const e = re(""), t = ["", "theme-blue", "theme-amber"];
    let s = 0;
    const n = () => {
        s = (s + 1) % t.length, e.value = t[s], document.body.className = e.value
    };
    return {
        currentTheme: e, toggleTheme: n, setupThemeToggle: () => {
            const l = o => {
                (o.key === "T" || o.key === "t") && n()
            };
            return document.addEventListener("keydown", l), () => document.removeEventListener("keydown", l)
        }
    }
}

function Ii() {
    const {cloneAsset: e} = Xr(), t = async (s, n, r = !0) => {
        if (s) {
            if (r && (s.innerHTML = ""), n.type === "container" && Array.isArray(n.value)) {
                const l = document.createElement("div");
                l.className = "component-container", n.style && (l.style.cssText = n.style);
                for (const o of n.value) await t(l, o, !1);
                s.appendChild(l)
            } else if (n.type === "text") {
                const l = document.createElement("span");
                l.className = "component-text", l.textContent = n.value, n.style && (l.style.cssText = n.style), s.appendChild(l)
            } else if (n.type === "assets") try {
                const l = await e(n.value);
                if (l) {
                    l.style.width = "calc(0.9 * var(--cell-size))", l.style.height = "calc(0.9 * var(--cell-size))", l.style.display = "block", l.style.maxWidth = "100%", l.style.maxHeight = "100%";
                    const o = l.querySelectorAll(".inner");
                    o.forEach(i => {
                        i.style.fill = "var(--foreground-color)"
                    }), n.style && (l.style.cssText += `; ${n.style}`), o.forEach(i => {
                        i.style.cssText += `; ${n.style}`
                    }), s.appendChild(l)
                }
            } catch (l) {
                console.error(`Failed to render asset ${n.value}:`, l);
                const o = document.createElement("span");
                o.className = "asset-placeholder", o.textContent = `[${n.value}]`, s.appendChild(o)
            }
            r && n.type !== "container" && n.style && (s.style.cssText += `; ${n.style}`)
        }
    };
    return {renderComponent: t}
}

const Pi = ["data-row", "data-col", "data-board", "data-cell-id"], Fi = {class: "cell-content"}, Ni = jt({
        __name: "GameCell",
        props: {row: {}, col: {}, cellState: {}, cellConfig: {}, boardName: {}, isHighlighted: {type: Boolean}},
        emits: ["click", "mouse-enter", "mouse-leave"],
        setup(e, {emit: t}) {
            const s = e, n = t, {renderComponent: r} = Ii(), l = re(), o = Ke(() => `${s.boardName}-${s.row}-${s.col}`),
                i = Ke(() => {
                    const p = [];
                    return s.cellState?.type === "revealed" && p.push("revealed"), s.isHighlighted && p.push("highlighted"), p
                }), f = () => {
                    n("click", s.row, s.col, s.boardName)
                }, d = () => {
                    n("mouse-enter", s.row, s.col, s.boardName, s.cellConfig)
                }, a = () => {
                    n("mouse-leave", s.row, s.col, s.boardName, s.cellConfig)
                }, h = async () => {
                    if (s.cellState?.type === "revealed" && l.value) if (s.cellConfig && s.cellConfig.component) {
                        if (await r(l.value, s.cellConfig.component, !0), s.cellConfig.overlayText) {
                            const p = document.createElement("div");
                            p.className = "cell-overlay", p.textContent = s.cellConfig.overlayText, l.value.appendChild(p)
                        }
                    } else {
                        if (s.cellState.value && typeof s.cellState.value == "object" && "type" in s.cellState.value) await r(l.value, s.cellState.value, !0); else {
                            const _ = {type: "text", value: s.cellState.value || "", style: ""};
                            await r(l.value, _, !0)
                        }
                        if (s.cellConfig?.overlayText) {
                            const p = document.createElement("div");
                            p.className = "cell-overlay", p.textContent = s.cellConfig.overlayText, l.value.appendChild(p)
                        }
                    }
                };
            return Rt(() => [s.cellState?.type, s.cellState?.value, s.cellConfig, s.isHighlighted], async () => {
                s.cellState?.type === "revealed" && (await gr(), h())
            }, {immediate: !0}), (p, _) => (Q(), ae("td", {
                class: as(["cell", i.value]),
                "data-row": p.row,
                "data-col": p.col,
                "data-board": p.boardName,
                "data-cell-id": o.value,
                onClick: f,
                onMouseenter: d,
                onMouseleave: a
            }, [F("div", Fi, [p.cellState?.type === "revealed" ? (Q(), ae("div", {
                key: 0,
                ref_key: "container",
                ref: l,
                class: "container"
            }, null, 512)) : Dt("", !0)])], 42, Pi))
        }
    }), Kt = (e, t) => {
        const s = e.__vccOpts || e;
        for (const [n, r] of t) s[n] = r;
        return s
    }, Di = Kt(Ni, [["__scopeId", "data-v-5310227e"]]), Li = {class: "game-table"}, ki = {class: "corner-cell"},
    Hi = {class: "row-header"}, ji = jt({
        __name: "GameTable",
        props: {GameTable: {}, rows: {}, cols: {}, boardName: {}, cellConfigs: {}},
        emits: ["cell-click"],
        setup(e) {
            const t = e, s = re(), n = (d, a) => {
                const h = Yr(d, a);
                return t.GameTable[h] || null
            }, r = (d, a) => {
                if (!t.cellConfigs || !t.boardName) return null;
                const {x: h, y: p} = Qr(d, a);
                return t.cellConfigs.find(_ => _.position.boardname === t.boardName && _.position.x === h && _.position.y === p) || null
            }, l = (d, a) => !1, o = (d, a, h, p) => {
                p && p.highlight && f(p.highlight, !0)
            }, i = (d, a, h, p) => {
                p && p.highlight && f(p.highlight, !1)
            }, f = (d, a) => {
                if (!s.value) return;
                let h = "";
                for (const [p, _] of Object.entries(d)) for (const [T, E] of _) {
                    const {row: k, col: R} = Mi(T, E), L = `[data-board="${p}"][data-row="${k}"][data-col="${R}"]`;
                    a && (h += `
          ${L} {
            background: var(--pointer-color, rgba(255, 255, 0, 0.3));
          }
        `)
                }
                s.value.textContent = h
            };
            return ps(() => {
                s.value = document.createElement("style"), s.value.type = "text/css", document.head.appendChild(s.value)
            }), gs(() => {
                s.value && s.value.parentNode && s.value.parentNode.removeChild(s.value)
            }), (d, a) => (Q(), ae("table", Li, [F("thead", null, [F("tr", null, [F("th", ki, Te(d.boardName), 1), (Q(!0), ae(fe, null, Yt(d.cols, h => (Q(), ae("th", {
                key: h,
                class: "col-header"
            }, Te(h), 1))), 128))])]), F("tbody", null, [(Q(!0), ae(fe, null, Yt(d.rows, h => (Q(), ae("tr", {key: h}, [F("th", Hi, Te(h), 1), (Q(!0), ae(fe, null, Yt(d.cols, p => (Q(), it(Di, {
                key: `${h}-${p}`,
                row: h,
                col: p,
                "cell-state": n(h, p),
                "cell-config": r(h, p),
                "board-name": d.boardName,
                "is-highlighted": l(),
                onClick: (_, T, E) => d.$emit("cell-click", _, T, E),
                onMouseEnter: o,
                onMouseLeave: i
            }, null, 8, ["row", "col", "cell-state", "cell-config", "board-name", "is-highlighted", "onClick"]))), 128))]))), 128))])]))
        }
    }), Bi = Kt(ji, [["__scopeId", "data-v-7154e912"]]), Ki = "/assets/flag.svg", Vi = "/assets/circle.svg",
    Ui = "/assets/double_arrow.svg", Gi = "/assets/arrow.svg", Wi = "/assets/cross.svg", qi = "/assets/star.svg",
    zi = {class: "game-overlay"}, Ji = {class: "rules"}, Yi = {class: "rule-line"}, Qi = {class: "mine-count"},
    Xi = {class: "remaining"}, Zi = {class: "bottom-info"}, ec = {class: "levelCount"}, tc = jt({
        __name: "Overlay",
        props: {levelCount: {default: "10/10"}, mineCount: {}, remainingMines: {}, remainingCells: {default: 21}},
        emits: ["flagClick", "circleClick", "doubleArrowClick", "arrowClick", "crossClick"],
        setup(e, {emit: t}) {
            const s = t, n = () => s("flagClick"), r = () => s("circleClick"), l = () => s("doubleArrowClick"),
                o = () => s("arrowClick"), i = () => s("crossClick");
            return (f, d) => (Q(), ae("div", zi, [F("div", Ji, [F("div", Yi, [d[0] || (d[0] = F("u", null, [F("span", {class: "rule-key"}, "[R]"), Be(" 总雷数")], -1)), d[1] || (d[1] = Be("：", -1)), F("span", Qi, Te(f.mineCount ?? "*"), 1), d[2] || (d[2] = Be(" (剩余雷数/格数：", -1)), F("span", Xi, Te(f.remainingMines ?? "*") + "/" + Te(f.remainingCells), 1), d[3] || (d[3] = Be(") ", -1))]), d[4] || (d[4] = F("div", {class: "rule-line"}, [F("u", null, [F("span", {class: "rule-key"}, "[Q]"), Be(" 无方")]), Be("：每个2x2区域内都至少有一个雷 ")], -1))]), F("div", {class: "controls"}, [F("button", {
                class: "control-btn",
                onClick: n
            }, d[5] || (d[5] = [F("img", {src: Ki}, null, -1)])), F("button", {
                class: "control-btn",
                onClick: r
            }, d[6] || (d[6] = [F("img", {src: Vi}, null, -1)])), F("button", {
                class: "control-btn",
                onClick: l
            }, d[7] || (d[7] = [F("img", {src: Ui}, null, -1)])), F("button", {
                class: "control-btn",
                onClick: o
            }, d[8] || (d[8] = [F("img", {src: Gi}, null, -1)])), F("button", {
                class: "control-btn",
                onClick: i
            }, d[9] || (d[9] = [F("img", {src: Wi}, null, -1)]))]), F("div", Zi, [d[10] || (d[10] = F("div", {class: "star-section"}, [F("img", {
                src: qi,
                class: "star-icon"
            }), F("span", {class: "game-info"}, "[Q]5x5-10-9991 (终极模式 +F +A)")], -1)), F("div", ec, Te(f.levelCount), 1)])]))
        }
    }), sc = Kt(tc, [["__scopeId", "data-v-938a755a"]]), nc = {class: "info-content"}, rc = {key: 0, class: "info-title"},
    lc = {class: "info-message"}, oc = {class: "info-actions"}, ic = jt({
        __name: "InfoOverlay",
        props: {
            visible: {type: Boolean, default: !1},
            title: {default: ""},
            message: {default: ""},
            confirmText: {default: "确定"},
            closeOnBackdrop: {type: Boolean, default: !0}
        },
        emits: ["confirm", "close", "update:visible"],
        setup(e, {emit: t}) {
            const s = e, n = t, r = () => {
                n("confirm"), n("update:visible", !1), n("close")
            }, l = () => {
                s.closeOnBackdrop && (n("update:visible", !1), n("close"))
            };
            return (o, i) => (Q(), it(zl, {to: "body"}, [o.visible ? (Q(), ae("div", {
                key: 0,
                class: "info-overlay",
                onClick: l
            }, [F("div", {
                class: "info-container", onClick: i[0] || (i[0] = bi(() => {
                }, ["stop"]))
            }, [F("div", nc, [o.title ? (Q(), ae("h3", rc, Te(o.title), 1)) : Dt("", !0), F("div", lc, [io(o.$slots, "default", {}, () => [Be(Te(o.message), 1)])])]), F("div", oc, [F("button", {
                class: "confirm-btn",
                type: "button",
                onClick: r
            }, Te(o.confirmText), 1)])])])) : Dt("", !0)]))
        }
    }), cc = Kt(ic, [["__scopeId", "data-v-f065770b"]]), fc = {class: "app-container"}, ac = {key: 0, class: "loading"},
    uc = {key: 1, class: "error"}, dc = {key: 2, class: "game-container"}, hc = jt({
        __name: "App", setup(e) {
            const {
                    isInitialized: t,
                    isLoading: s,
                    error: n,
                    allCells: r,
                    isGameOver: l,
                    gameOverReason: o,
                    initializeGame: i,
                    handleCellClick: f,
                    resetGame: d,
                    getAllBoardConfigs: a
                } = Ri(), {waitForAssets: h} = Xr(), {setupThemeToggle: p} = $i(), _ = re(!1),
                T = Ke(() => l.value ? o.value.includes("胜利") || o.value.includes("获胜") ? "🎉 恭喜获胜！" : "💥 游戏结束" : ""),
                E = Ke(() => o.value || "游戏已结束");
            Rt(l, Z => {
                Z && window.setTimeout(() => {
                    _.value = !0
                }, 500)
            });
            const k = async () => {
                _.value = !1, await d()
            }, R = Ke(() => "10/10"), L = Ke(() => {
            }), U = Ke(() => {
            }), w = Ke(() => 21), N = () => {
            }, J = () => {
            }, Y = () => {
            }, ee = () => {
            }, G = () => {
            };

            function le() {
                const Z = se => {
                    switch (se.key.toLowerCase()) {
                        case"r":
                            d();
                            break
                    }
                };
                return document.addEventListener("keydown", Z), () => document.removeEventListener("keydown", Z)
            }

            let he = null, Ee = null;
            return ps(async () => {
                await h(), await i(), he = p(), Ee = le()
            }), gs(() => {
                he && he(), Ee && Ee()
            }), (Z, se) => (Q(), ae("div", fc, [Ae(s) ? (Q(), ae("div", ac, "正在加载游戏配置...")) : Ae(n) ? (Q(), ae("div", uc, [Be(" 加载失败: " + Te(Ae(n)) + " ", 1), F("button", {onClick: se[0] || (se[0] = (...oe) => Ae(i) && Ae(i)(...oe))}, "重试")])) : Ae(t) ? (Q(), ae("div", dc, [(Q(!0), ae(fe, null, Yt(Ae(a)().filter(oe => oe !== null), oe => (Q(), it(Bi, {
                key: oe.name,
                GameTable: oe.gameBoard,
                rows: oe.labels.rows,
                cols: oe.labels.cols,
                "board-name": oe.name,
                "cell-configs": Ae(r),
                onCellClick: se[1] || (se[1] = (ne, H, V) => Ae(f)(V, ne, H))
            }, null, 8, ["GameTable", "rows", "cols", "board-name", "cell-configs"]))), 128))])) : Dt("", !0), Ae(t) ? (Q(), it(sc, {
                key: 3,
                levelCount: R.value,
                "mine-count": L.value,
                "remaining-mines": U.value,
                "remaining-cells": w.value,
                onFlagClick: N,
                onCircleClick: J,
                onDoubleArrowClick: Y,
                onArrowClick: ee,
                onCrossClick: G
            }, null, 8, ["levelCount", "mine-count", "remaining-mines", "remaining-cells"])) : Dt("", !0), Me(cc, {
                visible: _.value,
                "onUpdate:visible": se[2] || (se[2] = oe => _.value = oe),
                title: T.value,
                message: E.value,
                "confirm-text": "重新开始",
                onConfirm: k
            }, null, 8, ["visible", "title", "message"])]))
        }
    }), pc = Kt(hc, [["__scopeId", "data-v-8e87b4d0"]]);
xi(pc).mount("#app");
